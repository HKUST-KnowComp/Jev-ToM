# Data access

The packaged collections use UTF-8 JSON Lines compressed with gzip. Each benchmark folder separates questions from ground-truth keys. Python's standard library can read every file directly, without unpacking the whole repository.

| Path | Contents |
| --- | --- |
| `primary/` | 11,117 frozen primary questions, source keys and corrected application mapping |
| `reason_pairs/` | 4,761 accepted materials and 38,088 condition/order questions |
| `reason_controls/` | 25,704 six-condition questions, with retained-main membership in the keys |
| `feedback_extension/` | 800 native questions, 400 pair definitions and exact feedback suffix templates |

Inspect the first primary question:

```sh
python3 -c 'import gzip,json; f=gzip.open("data/primary/bigtom/questions.jsonl.gz","rt",encoding="utf-8"); print(json.dumps(json.loads(next(f)),ensure_ascii=False,indent=2))'
```

Read [dataset scope and counts](../docs/DATASETS.md) and the [field schema](../docs/SCHEMA.md) before constructing inputs. The source keys, historical strata and machine-review metadata are evaluation metadata, not model input.

These are frozen evaluated subsets of existing benchmarks. The six operational capabilities are knowledge access, beliefs, goals/desires/intentions, emotions, social pragmatics and mental-state application. Their coverage differs by benchmark, and a question may map to multiple capabilities.

Upstream terms and evaluation-only notices remain in force. This local package does not grant broader rights to the source questions, contexts or candidate answers. See the [source-by-source notices](../notices/README.md).
