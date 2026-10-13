# Dataset scope

| Benchmark | Primary questions | Accepted reason materials | Reason-pair variants | Six-condition variants | Additional feedback questions |
| --- | --- | --- | --- | --- | --- |
| BigToM | 1200 | 422 | 3376 | 1296 | 400 |
| OpenToM | 2533 | 1072 | 8576 | 9804 | 0 |
| ToMBench | 730 | 344 | 2752 | 1536 | 0 |
| SimpleToM | 891 | 548 | 4384 | 4416 | 400 |
| FANToM | 1805 | 524 | 4192 | 3576 | 0 |
| ToMATO | 1396 | 633 | 5064 | 2016 | 0 |
| CogToM | 2154 | 1073 | 8584 | 2196 | 0 |
| Hi-ToM | 154 | 53 | 424 | 240 | 0 |
| ToMi | 254 | 92 | 736 | 624 | 0 |

The primary workload contains 11,117 frozen questions. It is the exact evaluated sample, rather than every source benchmark's complete release. It omits the previously fixed 50 BigToM source-problem items. Benchmark IDs identify OpenToM discrete and FANToM short-context subsets explicitly. Controls and unassigned questions remain in benchmark totals.

The reason-pair collection contains 4,761 accepted materials (1,803 reused and 2,958 newly prepared) on existing primary questions. Four conditions and two saved orders give 38,088 variant questions. `joint` crosses all original answers with all reasons, `aligned` preserves the attached pairs, `answer_only` selects among answers, and `reason_only` selects among reasons. The orders are an ID-hashed permutation and its reversal, rather than exhaustive position balancing. `material_coverage.csv` preserves accepted/rejected/error coverage for all 11,117 candidate source questions.

These reasons were constructed with the source answer key and machine-reviewed. The keyed reason is the reason attached to the source reference answer. This does not establish that every reason is independently human-validated or semantically unique. Newly prepared reasons are for existing questions, rather than a new unseen test set. Supplied reasons are option-distraction interventions.

The six-condition collection preserves all 25,704 evaluated variants from 2,142 initial materials. The main paper uses the 1,803 later approved materials (21,636 variants), identified by `main_analysis_retained` in each answer-key row. The conditions are bare, neutral, aligned, swapped, both_consistent and both_inconsistent, each in original and reversed option order. Historical correct/error strata refer to earlier selections, rather than fresh no-reason correctness. The selected population was enriched for historical errors. This is a separately scoped Jev experiment, not an additional 12-model primary evaluation.

The feedback extension contains 800 additional native questions: 400 belief/awareness questions paired with 400 action/behavior targets, split equally between BigToM and SimpleToM. Families are disjoint from the primary sample and the earlier discovery study. It uses the five typed models, with original, question_only, predicted_state and flipped_state target conditions. Saved upstream choices supply the model-dependent feedback. Flipped feedback supplies the other binary option and is not necessarily wrong. SimpleToM upstream references are all No. This bounded action-selection experiment does not evaluate an end-to-end assistant.
