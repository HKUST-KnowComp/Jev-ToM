# Data and answer-key schema

Files are UTF-8 JSON Lines compressed with gzip. Every benchmark has matching `questions.jsonl.gz` and `ground_truth.jsonl.gz` files joined by `id`. Indices are zero-based. Original context, question text, candidate strings and candidate order are preserved. Rows may be sorted by ID for export, which does not reorder any question's options.

- Question rows contain `id`, `source_dataset`, `family_id`, `state`, `question`, `options` and available native source identifiers. Only `state`, `question` and `options` form model inputs.
- Key rows contain `id`, `source_dataset`, `gold_option_index` and `gold_option_text`. Never send key rows, reference labels or historical strata to an evaluated model.
- Reason-pair questions add `source_id`, `arm`, `order`, `option_components`, `original_option_count` and the archived `material_sha256`. Each component contains `answer_index` and `reason_index` into the original options/reasons. Null means the component is absent. Material hashes refer to the full archived records, whose prompts and traces are not copied into this package. The package manifest checks the actual distributed files.
- Reason-pair keys add `original_gold_index` and `scoring_target`. `joint` strict exact match requires the keyed answer and the keyed reason together. Answer-component accuracy checks only the answer index and is explicitly separate. `reason_only` checks the keyed reason index.
- Six-condition questions add `answer_options` and `reasons`. Their gold index identifies the correct original answer, including when its attached reason is distracting. `gold_answer_text` stores that answer. Keys identify the retained main population and historical stratum.
- Primary prediction rows store the frozen parsed `status` and `predicted_index`. Invalid outcomes have a null index and count as wrong, including remaining SmolLM3 errors. This is a sanitized outcome export, not the full raw API response/attempt journal.

## Reading a benchmark

```python
import gzip, json
from pathlib import Path

root = Path("data/reason_pairs/bigtom")
with gzip.open(root / "questions.jsonl.gz", "rt", encoding="utf-8") as f:
    questions = {r["id"]: r for r in map(json.loads, f)}
with gzip.open(root / "ground_truth.jsonl.gz", "rt", encoding="utf-8") as f:
    answers = {r["id"]: r for r in map(json.loads, f)}
qid = next(iter(questions))
assert questions[qid]["options"][answers[qid]["gold_option_index"]] == answers[qid]["gold_option_text"]
```

## Reconstructing feedback inputs

`units.jsonl.gz` links each upstream question to its target. `prompts.json` contains the exact saved suffix templates. Original and mental_state queries use their base inputs. For the other conditions, append the formatted suffix to the target's `state` (not its `question`). Fill `upstream_question` from the paired upstream row. For predicted_state, fill `upstream_selected_option_text` from that model's saved mental_state prediction. For flipped_state, use the other upstream candidate. `results/feedback_predictions/` preserves the choices and dependencies needed for all five models. The wording continues to attribute the injected option to the model as in the original experimental framing. Candidate strings/order remain unchanged.
