# Result tables

- `benchmark_performance.md` and `.csv`: all 12 current models by all nine benchmarks and Overall.
- `primary_by_benchmark.csv`: 108 exact benchmark cells with counts, validity and positional macro-F1.
- `primary_overall.csv`: exact benchmark-equal overall scores.
- `capability_performance.csv`: six capability scores with corrected application mapping.
- `primary_predictions/`: all 133,404 saved primary model/question outcomes, sufficient to replay accuracy.
- `reason_pairs_by_benchmark.csv`: eight active follow-up models, four conditions, nine benchmarks (288 cells). Joint accuracy in this table requires both components.
- `reason_answer_component.csv`: main reason analysis's answer-component scores, equally weighted across nine benchmarks. Crossed answer correctness does not require reason correctness.
- `reason_controls_by_benchmark.csv`: six-condition source scores, including both the initial and later retained populations, with their historical strata. These are pooled within each source.
- `feedback_extension.csv` and `feedback_predictions/`: five-model, four-condition action macros and all 10,000 saved upstream/target outcomes. Macros equally weight BigToM and SimpleToM.

Primary benchmark accuracy is correct/all questions, treating invalid responses as errors. Overall is the arithmetic mean of nine benchmark accuracies, rather than pooled accuracy. Capability accuracy first averages within each mapped benchmark, then equally averages those benchmarks with eligible items. Capability labels may overlap. The positional macro-F1 column uses gold-supported original candidate positions, rather than native semantic classes. Question, benchmark and capability denominators are not interchangeable.

The current primary comparison follows the paper's frozen outcome cohort. Only the completed SmolLM3 failed-item overlay is included, retaining every valid original. Other later repairs and timing runs are not merged. The full repair/exclusion history remains in provenance. Model selection was post-evaluation. Published reference-only scores are not our measurements.

The offline verifier replays primary accuracies and feedback macros from the distributed choices and keys. Reason/capability tables are exports of separately saved summaries. Full raw-response reproduction, material-generation reruns, statistical interval regeneration and deployment timing are outside this package's supplied replay.
