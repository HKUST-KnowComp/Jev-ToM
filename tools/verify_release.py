"""Offline integrity and answer-key checks for the standalone GitHub package."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
from collections import Counter
from pathlib import Path


def read_rows(path):
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt', encoding='utf-8') as handle:
        return [json.loads(line) for line in handle if line.strip()]


def unique(rows):
    result = {row['id']: row for row in rows}
    assert len(result) == len(rows), 'Duplicate question/answer IDs'
    return result


def verify(root):
    sums = json.loads((root / 'SHA256SUMS.json').read_text())
    actual_files = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()
                    and p.name != 'SHA256SUMS.json' and '.git' not in p.parts
                    and '__pycache__' not in p.parts and p.name != '.DS_Store'}
    assert actual_files == set(sums), 'Unlisted or missing package files'
    for name, expected in sums.items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
    manifest = json.loads((root / 'manifest.json').read_text())
    primary, gold, all_counts = {}, {}, {}
    pair_material_ids, retained_control_ids = set(), set()
    for collection, info in manifest['collections'].items():
        count = 0
        for source, files in info['benchmarks'].items():
            qs = unique(read_rows(root / files['questions']))
            gs = unique(read_rows(root / files['ground_truth']))
            assert set(qs) == set(gs) and len(qs) == files['n'], (collection, source)
            for qid, q in qs.items():
                g = gs[qid]
                assert not any(k in q for k in ('gold', 'gold_option_index', 'original_gold_index',
                                               'historical_predicted', 'foil_answer'))
                assert q['source_dataset'] == source and q['options']
                assert len(set(q['options'])) == len(q['options']), qid
                idx = g['gold_option_index']
                assert type(idx) is int and 0 <= idx < len(q['options']), qid
                assert q['options'][idx] == g['gold_option_text'], qid
                assert g['source_dataset'] == source, qid
                if collection == 'primary':
                    assert qid not in primary
                    primary[qid], gold[qid] = q, g
                elif collection == 'reason_pairs':
                    source_q, source_g = primary[q['source_id']], gold[q['source_id']]
                    assert q['state'] == source_q['state']
                    og = source_g['gold_option_index']
                    assert g['original_gold_index'] == og
                    comps = q['option_components']
                    assert len(comps) == len(q['options'])
                    winners = [i for i, c in enumerate(comps)
                               if all(c[k] is None or c[k] == og
                                      for k in ('answer_index', 'reason_index'))]
                    assert winners == [idx], qid
                    assert q['original_option_count'] == len(source_q['options'])
                    pair_material_ids.add(q['source_id'])
                elif collection == 'reason_controls':
                    source_q = primary[q['source_id']]
                    assert q['state'] == source_q['state']
                    assert q['answer_options'][idx] == gold[q['source_id']]['gold_option_text']
                    if g['main_analysis_retained']:
                        retained_control_ids.add(q['source_id'])
            count += len(qs)
        assert count == info['n'], collection
        all_counts[collection] = count
    assert len(primary) == 11117 and len(pair_material_ids) == 4761
    assert len(retained_control_ids) == 1803
    reused_ids = set()
    for source, files in manifest['collections']['reason_pairs']['benchmarks'].items():
        mats = unique(read_rows(root / files['materials']))
        reused_ids.update(qid for qid, m in mats.items() if m['material_stratum'] == 'reused')
        qs = read_rows(root / files['questions'])
        assert set(mats) == {q['source_id'] for q in qs}
        for q in qs:
            reasons = mats[q['source_id']]['reasons']
            options = primary[q['source_id']]['options']
            for text, c in zip(q['options'], q['option_components']):
                ai, ri = c['answer_index'], c['reason_index']
                wanted = (reasons[ri] if ai is None else options[ai] if ri is None
                          else f'Answer: {options[ai]}\nReason: {reasons[ri]}')
                assert wanted == text, q['id']
            assert mats[q['source_id']]['machine_review_approved'] is True
        groups = Counter((q['source_id'], q['arm']) for q in qs)
        assert all(n == 2 for n in groups.values())
        assert len(groups) == len(mats) * 4
    assert retained_control_ids == reused_ids
    for files in manifest['collections']['reason_controls']['benchmarks'].values():
        qs = read_rows(root / files['questions'])
        groups = Counter(q['source_id'] for q in qs)
        assert all(n == 12 for n in groups.values())

    models = json.loads((root / 'models/models.json').read_text())
    assert len(models) == 12 and Counter(m['type'] for m in models) == {
        'typed_decision': 5, 'generative_llm': 7}
    cells = list(csv.DictReader((root / 'results/primary_by_benchmark.csv').open()))
    assert len(cells) == 108
    overall = {r['model_id']: r for r in csv.DictReader((root / 'results/primary_overall.csv').open())}
    wide = {r['model_id']: r for r in csv.DictReader((root / 'results/benchmark_performance.csv').open())}
    replays = 0
    for model in models:
        mid = model['model_id']
        preds = unique(read_rows(root / model['primary_predictions']))
        assert set(preds) == set(primary), mid
        scores = []
        for source in manifest['benchmark_order']:
            items = [qid for qid, q in primary.items() if q['source_dataset'] == source]
            correct, valid = 0, 0
            for qid in items:
                r = preds[qid]
                assert r['model_id'] == mid
                if r['status'] == 'ok':
                    pi = r['predicted_index']
                    assert type(pi) is int and 0 <= pi < len(primary[qid]['options'])
                    valid += 1
                    correct += pi == gold[qid]['gold_option_index']
                else:
                    assert r['predicted_index'] is None
            cell = next(c for c in cells if c['model_id'] == mid and c['benchmark_id'] == source)
            score = 100 * correct / len(items)
            assert int(cell['n']) == len(items) and int(cell['correct']) == correct
            assert int(cell['valid']) == valid
            assert math.isclose(float(cell['accuracy_pct']), score, abs_tol=1e-10)
            assert math.isclose(float(wide[mid][source]), score, abs_tol=1e-10)
            scores.append(score)
            replays += 1
        assert math.isclose(sum(scores) / 9, float(overall[mid]['overall_accuracy_pct']), abs_tol=1e-10)
        assert math.isclose(sum(scores) / 9, float(wide[mid]['overall_accuracy_pct']), abs_tol=1e-10)

    feedback_q = {}
    feedback_g = {}
    for files in manifest['collections']['feedback_extension']['benchmarks'].values():
        feedback_q.update(unique(read_rows(root / files['questions'])))
        feedback_g.update(unique(read_rows(root / files['ground_truth'])))
    units = read_rows(root / 'data/feedback_extension/units.jsonl.gz')
    assert len(units) == 400
    assert not {q['family_id'] for q in feedback_q.values()} & {q['family_id'] for q in primary.values()}
    referenced = []
    for u in units:
        uq = feedback_q[u['upstream_id']]
        assert len(uq['options']) == 2
        for tid in u['target_ids']:
            tq = feedback_q[tid]
            assert tq['state'] == uq['state'] and tq['family_id'] == uq['family_id']
        referenced.extend([u['upstream_id']] + u['target_ids'])
    assert len(set(referenced)) == len(referenced) == 800
    feedback_cells = list(csv.DictReader((root / 'results/feedback_extension.csv').open()))
    feedback_outcomes = 0
    for m in [m for m in models if m['type'] == 'typed_decision']:
        rows = read_rows(root / f"results/feedback_predictions/{m['slug']}.jsonl.gz")
        assert len(rows) == 2000 and len({r['key'] for r in rows}) == 2000
        for arm in ('original', 'question_only', 'predicted_state', 'flipped_state'):
            by_source = []
            for source in ('bigtom', 'simpletom'):
                rs = [r for r in rows if r['arm'] == arm and r['source_dataset'] == source]
                assert len(rs) == 200
                score = 100 * sum(r['status'] == 'ok' and
                                 r['predicted_index'] == feedback_g[r['id']]['gold_option_index']
                                 for r in rs) / 200
                by_source.append(score)
            cell = next(r for r in feedback_cells if r['model_id'] == m['model_id'] and r['arm'] == arm)
            assert math.isclose(sum(by_source) / 2, float(cell['accuracy_pct']), abs_tol=1e-10)
        feedback_outcomes += len(rows)
    return dict(status='passed', checked_files=len(sums), question_counts=all_counts,
                primary_benchmark_cells_replayed=replays, primary_overall_scores_replayed=12,
                feedback_outcomes_checked=feedback_outcomes, new_inference_calls=0,
                published=False)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args()
    print(json.dumps(verify(args.root.resolve()), indent=2))
