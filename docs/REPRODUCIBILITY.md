# Reproducing the distributed results

The repository is an offline data and parsed-result package. Python 3.10 or newer is sufficient, with no third-party dependencies or model credentials.

## Integrity and saved-result replay

From the repository root:

```sh
python3 tools/verify_release.py
```

The verifier checks distributed file hashes, question/key alignment, candidate-component mappings, retained reason-material membership, 108 primary benchmark cells, 12 benchmark-equal overall scores and the five-model feedback scores from 10,000 saved outcomes.

`manifest.json` preserves the original 2026-10-10 data-export snapshot. Archived input hashes identify the original research files, which are not required to use this standalone package. `SHA256SUMS.json` identifies the current distributed files, excluding itself and Git metadata.

## Score one model

```sh
python3 tools/score_primary.py --predictions results/primary_predictions/jev.jsonl.gz
```

The output reports counts, strict exact-match accuracy for every benchmark, and the equal-benchmark overall score. For Jev, the displayed overall score rounds to **73.2%**.

To score another saved prediction file, use the same command with its path. A file must contain exactly one row for each of the 11,117 frozen primary IDs, with these fields:

```json
{"id": "an-existing-question-id", "status": "ok", "predicted_index": 0}
```

This is a schema example. Use actual IDs from the question files and zero-based indices into their unchanged `options`. For a failed or invalid response, use a nonempty status other than `ok` and `"predicted_index": null`. An optional `model_id` must have one consistent value throughout the file. Missing IDs, extra IDs, duplicate IDs and malformed indices are rejected to prevent silent changes to the denominator. Invalid outcomes count as wrong.

This scorer consumes choices that have already passed the intended model-specific output parser. It does not validate raw model responses, probability sums or output schemas on behalf of a new model. It also does not reconstruct the historical parser from a choice alone.

## What can be reproduced here

| Material or result | Supplied coverage |
| --- | --- |
| Primary benchmark and overall accuracy | Full replay from 133,404 parsed outcomes and separate keys |
| Five-model feedback accuracy | Full replay from 10,000 parsed upstream/target outcomes |
| Reason inputs and condition/order mappings | Distributed questions, materials and keys |
| Capability, reason-pair and six-condition summaries | Exact exported tables, not full per-question result replay |
| Confidence analyses and candidate-load diagnostics | Not reproduced by the supplied tools |
| Human annotation stages | Not included in this package |
| Statistical intervals and family resampling | Not implemented in this package |
| Costs, latency and serving environment | Not reconstructed by this package |

The manuscript's broader release inventory describes planned materials. Coverage of this repository is listed above. Full provider attempt journals, credentials, model weights and original generation/review records are not included. The tools make no model calls.

## Figures

The README displays the current manuscript's capability-coverage and primary capability-atlas images. These are figure assets, not a separately rebuilt score computation. The twelve-model primary table and `results/capability_performance.csv` remain the numerical references.

## Source terms

The original questions and contexts keep their source-specific terms. Consult [source notices](../notices/README.md) before using or redistributing them. The authors' CC BY 4.0 designation covers original releasable contributions and does not relicense the source benchmarks or models.
