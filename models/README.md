# Model list

The primary comparison contains five typed decision models and seven generative LLMs. Hosted identities are provider-reported. The typed models use their own native interfaces, and this grouping does not assert a shared architecture.

| Model | Canonical ID | Type | Deployment | Settings |
| --- | --- | --- | --- | --- |
| Jev-1.13 | `typesafe/jev-1.13` | Typed | OpenRouter decision API | Native choice interface |
| Open-Jev-2B | `ZefanCai/Open-Jev-2B` | Typed | Local MLX/MPS on Apple M4 Pro (48 GiB) | Native choice interface and checkpoint-specific settings, artifact hashes recorded where a checkpoint revision is absent |
| Valen | `Valen-Team/Valen-Preview-0923` | Typed | Local MLX/MPS on Apple M4 Pro (48 GiB) | Native choice interface and checkpoint-specific settings |
| Tiny-Jev | `lostargon/Tiny-Jev` | Typed | Local MLX/MPS on Apple M4 Pro (48 GiB) | Native choice interface and checkpoint-specific settings |
| OpenJev-0.6B | `IamBusy/OpenJev-0.6B` | Typed | Local MLX/MPS on Apple M4 Pro (48 GiB) | Native choice interface and checkpoint-specific settings |
| GPT-4.1-nano | `gpt-4.1-nano-2025-04-14` | LLM | OpenLux hosted API, provider-reported identity | Temperature 0, maximum 32 output tokens |
| GPT-4o-mini | `gpt-4o-mini-2024-07-18` | LLM | OpenLux hosted API, provider-reported identity | Temperature 0, maximum 32 output tokens |
| GPT-5.6-Luna | `gpt-5.6-luna` | LLM | Codex CLI, isolated session per question | Low reasoning effort, tools disabled, no 32-token hard cap |
| Llama-3.1-8B | `meta-llama/llama-3.1-8b-instruct` | LLM | OpenRouter, DeepInfra FP8 | Temperature 0, maximum 32 output tokens |
| DeepSeek-V4-Flash | `deepseek/deepseek-v4-flash-0731` | LLM | OpenRouter, DeepInfra FP8 | Temperature 0, maximum 32 output tokens, reasoning disabled |
| GPT-3.5-1106 | `gpt-3.5-turbo-1106` | LLM | OpenLux hosted API, provider-reported identity | Temperature 0, maximum 32 output tokens |
| SmolLM3-3B | `HuggingFaceTB/SmolLM3-3B` | LLM | Local MLX on Apple M4 Pro (48 GiB) | Non-thinking greedy decoding, 32 output tokens, batch size 4, 16,384-token input limit |

`models.json` records exact returned versions, available checkpoint revisions, artifact hashes, runtime settings, scope membership and saved-result provenance. A null checkpoint revision means it was not recorded here, rather than a substituted foundation revision.

The archived selection ledger is in `model_disposition_history.csv`. It retains excluded, supplementary, unrun and published-reference-only entries. These entries are not additional rows in the current primary comparison. Selection occurred after evaluation.
