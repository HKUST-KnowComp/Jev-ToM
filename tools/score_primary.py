"""Score parsed primary choices offline against the frozen 11,117-question sample."""
from __future__ import annotations

import argparse
import gzip
import json
import sys
from pathlib import Path


def read_rows(path: Path) -> dict:
    opener = gzip.open if path.suffix == ".gz" else open
    rows = {}
    with opener(path, "rt", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: expected a JSON object")
            qid = row.get("id")
            if not isinstance(qid, str) or not qid:
                raise ValueError(f"{path}:{line_number}: missing string id")
            if qid in rows:
                raise ValueError(f"{path}:{line_number}: duplicate id {qid}")
            rows[qid] = row
    return rows


def score(root: Path, prediction_path: Path) -> dict:
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    predictions = read_rows(prediction_path)
    benchmarks = manifest["collections"]["primary"]["benchmarks"]
    questions, answers = {}, {}
    for source in manifest["benchmark_order"]:
        questions[source] = read_rows(root / benchmarks[source]["questions"])
        answers[source] = read_rows(root / benchmarks[source]["ground_truth"])
        if questions[source].keys() != answers[source].keys():
            raise ValueError(f"Question/key mismatch in {source}")
    expected_ids = {qid for qs in questions.values() for qid in qs}
    missing = expected_ids - predictions.keys()
    extra = predictions.keys() - expected_ids
    if missing or extra:
        raise ValueError(
            f"Prediction IDs must match the full primary sample: "
            f"{len(missing)} missing, {len(extra)} unexpected"
        )
    for qid, row in predictions.items():
        if row.get("model_id") is not None and not isinstance(row["model_id"], str):
            raise ValueError(f"{qid}: model_id must be a string when present")
    model_ids = {row.get("model_id") for row in predictions.values()}
    if len(model_ids) != 1:
        raise ValueError("The prediction file mixes model_id values")
    results = []
    for source in manifest["benchmark_order"]:
        correct = valid = 0
        for qid, question in questions[source].items():
            prediction = predictions[qid]
            status = prediction.get("status")
            selected = prediction.get("predicted_index")
            if not isinstance(status, str) or not status:
                raise ValueError(f"{qid}: missing status")
            if status == "ok":
                if type(selected) is not int or not 0 <= selected < len(question["options"]):
                    raise ValueError(f"{qid}: status=ok requires an in-range integer predicted_index")
                valid += 1
                correct += selected == answers[source][qid]["gold_option_index"]
            elif selected is not None:
                raise ValueError(f"{qid}: invalid outcomes must have a null predicted_index")
        n = len(questions[source])
        results.append({"benchmark_id": source, "n": n, "valid": valid,
                        "invalid": n - valid, "correct": correct,
                        "accuracy_pct": 100 * correct / n})
    return {
        "model_id": next(iter(model_ids)),
        "scoring": "Parsed strict exact match, invalid outcomes count as wrong",
        "n": len(expected_ids),
        "benchmarks": results,
        "overall_accuracy_pct": sum(r["accuracy_pct"] for r in results) / len(results),
        "aggregation": "Equal weight for each of the nine benchmarks",
        "new_inference_calls": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions", type=Path, required=True,
                        help="JSONL or gzip JSONL with id, status and predicted_index")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="Repository root containing manifest.json")
    args = parser.parse_args()
    try:
        result = score(args.root.resolve(), args.predictions)
    except (ValueError, KeyError, OSError) as error:
        parser.exit(2, f"Scoring failed: {error}\n")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2, allow_nan=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
