# CogToM

[English](README.md) | [中文](README_ZH.md)

This repository contains the companion code and benchmark data for the paper **CogToM: A Comprehensive Theory of Mind Benchmark inspired by Human Cognition for Large Language Models**.

CogToM is a bilingual Theory of Mind benchmark designed to evaluate how large language models reason about mental states, emotions, intentions, beliefs, knowledge, and other cognition-inspired ToM abilities. The code in this repository provides a configurable evaluation pipeline for running LLMs on CogToM with different datasets, prompts, model backends, and generation settings.

Paper: <https://arxiv.org/abs/2601.15628>

## Repository Structure

```text
.
├── main.py                    # Main entry point for a single evaluation run
├── batch_run.py               # Batch runner for multiple model/prompt combinations
├── vllm.sh                    # Example vLLM serving command
├── configs/
│   ├── datasets/              # Dataset configs
│   ├── llms/                  # LLM backend configs
│   ├── prompts/               # Prompt template configs
│   └── gen_config.yaml        # Generation parameters
├── data/
│   ├── CogToM-en.jsonl        # English CogToM benchmark data
│   └── CogToM-zh.jsonl        # Chinese CogToM benchmark data
└── src/
    ├── dataset.py             # Dataset loading and option permutation
    ├── evaluator.py           # Answer extraction and scoring
    ├── llm.py                 # OpenAI-compatible LLM wrapper
    ├── pipeline.py            # Parallel evaluation pipeline
    └── prompt.py              # Prompt construction
```

## Clone

```bash
git clone https://github.com/Beijing-AISI/CogToM.git
cd CogToM
pip install -r requirements.txt
```

## API Settings

The evaluation code uses an OpenAI-compatible Chat Completions interface. We recommend using a `.env` file to configure the required environment variables:

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=your_base_url
```

Example model config for `gpt-4o-mini`:

```yaml
llm_type: "OpenAILLM"
model_name: "gpt-4o-mini"
```

If `base_url` and `api_key` are not explicitly specified in a model config, the code will use `OPENAI_BASE_URL` and `OPENAI_API_KEY` from the environment.

For local OpenAI-compatible services such as vLLM, set `base_url` and `api_key` in the corresponding model config under `configs/llms/`:

```yaml
llm_type: "OpenAILLM"
model_name: "meta-llama/Llama-3.1-8B-Instruct"
base_url: "http://127.0.0.1:8000/v1"
api_key: "sk-none"
```

An example vLLM launch command is provided in `vllm.sh`.

## Quick Start

Run with the default settings:

```bash
python main.py
```

Run a small English evaluation:

```bash
python main.py \
  --llm-config configs/llms/gpt-5.1.yaml \
  --prompt-config configs/prompts/vanilla-en.yaml \
  --dataset-config configs/datasets/cogtom-en.yaml \
  --run-name gpt-5.1_vanilla-en_debug \
  --limit 5 \
  --workers 4
```

Run a Chinese evaluation:

```bash
python main.py \
  --llm-config configs/llms/gpt-5.1.yaml \
  --prompt-config configs/prompts/vanilla-zh.yaml \
  --dataset-config configs/datasets/cogtom-zh.yaml \
  --run-name gpt-5.1_vanilla-zh \
  --workers 8
```

Run a Chinese chain-of-thought prompt setting:

```bash
python main.py \
  --llm-config configs/llms/gpt-5.1.yaml \
  --prompt-config configs/prompts/cot-zh.yaml \
  --dataset-config configs/datasets/cogtom-zh.yaml \
  --run-name gpt-5.1_cot-zh \
  --workers 8
```

Useful `main.py` arguments:

- `--dataset-config`: path to the dataset config. Default: `configs/datasets/cogtom-zh.yaml`.
- `--prompt-config`: path to the prompt config. Default: `configs/prompts/vanilla-zh.yaml`.
- `--llm-config`: path to the LLM client config. Default: `configs/llms/llama-3.1-8b-it.yaml`.
- `--gen-config`: path to the generation parameter config. Default: `configs/gen_config.yaml`.
- `--output-dir`: directory for JSONL outputs. Default: `results`.
- `--run-name`: name of the run and output file stem. When set to `my_run`, results are written to `results/my_run.jsonl`.
- `--limit`: maximum number of question groups to evaluate. Default: `-1`, meaning no limit.
- `--workers`: number of parallel worker threads. Default: `16`.
- `--seed`: random seed for option permutations and reproducibility. Default: `42`.
- `--force`: ignore existing progress and rerun from scratch.

## Batch Evaluation

`batch_run.py` traverses all LLM config files and prompt config files, builds their Cartesian product, and launches one evaluation run for each model-prompt pair. Experiments are executed in parallel according to `--max-parallel`. For each run, the script automatically generates `run_name` as `{llm_config_name}_{prompt_config_name}`.

To run multiple LLM and prompt combinations:

```bash
python batch_run.py \
  --llm-configs configs/llms \
  --prompt-configs configs/prompts \
  --max-parallel 4
```

`batch_run.py` infers the dataset language from the prompt config name:

- prompt names containing `zh` use `configs/datasets/cogtom-zh.yaml`
- prompt names containing `en` use `configs/datasets/cogtom-en.yaml`

Useful `batch_run.py` arguments:

- `--llm-configs`: directory containing LLM config files. Default: `configs/llms`.
- `--prompt-configs`: directory containing prompt config files. Default: `configs/prompts`.
- `--output-dir`: directory for all generated JSONL outputs. Default: `results`.
- `--max-parallel`: maximum number of experiments to run in parallel. Default: `4`.

## Configuration Files

CogToM uses YAML files to keep experiment settings separate from the evaluation code. A run is defined by four types of configuration files: dataset configs select the benchmark split, LLM configs select the model backend, generation configs control decoding parameters, and prompt configs define how each item is presented to the model. These files can be swapped through command-line arguments such as `--dataset-config`, `--llm-config`, `--gen-config`, and `--prompt-config`.

Dataset config example:

```yaml
dataset_type: "TomDataset"
file_path: "./data/CogToM-en.jsonl"
limit: -1
```

LLM config example:

```yaml
llm_type: "OpenAILLM"
model_name: "gpt-5.1"
```

Generation config example:

```yaml
temperature: 0.0
max_tokens: 4096
seed: 42
```

Prompt configs define the system prompt, user template, template name, and option formatting. The user template can reference dataset fields such as `{scene}`, `{question}`, and `{options_str}`.

## Data Format

CogToM data files are JSONL files. Each line is one multiple-choice item:

```json
{
  "id": "sample_id",
  "category": "Category",
  "subcategory": "Subcategory",
  "scene": "Scenario text",
  "question": "Question text",
  "options": {
    "A": "Option A",
    "B": "Option B",
    "C": "Option C",
    "D": "Option D"
  },
  "answer": "B"
}
```

During evaluation, each item is expanded into several option-order variants. The correct answer label is recomputed after permutation, allowing the pipeline to measure both answer accuracy and semantic consistency.

## Output Format

Each evaluated item is written as one JSON object. Important fields include:

- `id`: sample identifier.
- `category` and `subcategory`: CogToM task labels.
- `group_accuracy`: average accuracy across option variants for the item.
- `is_consistent`: whether the model selected the same semantic option across valid variants.
- `variant_count`: number of evaluated variants.
- `details`: per-variant raw output, extracted label, correctness, and retry count.

If an output file for the same run already exists, `main.py` reads processed sample IDs and skips them by default. Use `--force` to rerun all samples.

## Citation

If you use CogToM in your research, please cite:

```bibtex
@misc{tong2026cogtom,
  title        = {CogToM: A Comprehensive Theory of Mind Benchmark inspired by Human Cognition for Large Language Models},
  author       = {Tong, Haibo and Yue, Zeyang and Zhao, Feifei and Lin, Erliang and Jia, Lu and Chen, Ruolin and Sun, Yinqian and Zhang, Qian and Zeng, Yi},
  year         = {2026},
  eprint       = {2601.15628},
  archivePrefix = {arXiv},
  url          = {https://arxiv.org/abs/2601.15628}
}
```
