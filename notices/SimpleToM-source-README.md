---
annotations_creators:
- found
language_creators:
- found
language:
- en
license:
- odc-by
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
configs:
- config_name: mental-state-qa
  data_files: 
  - split: test
    path: mental-state-qa/test.jsonl
- config_name: behavior-qa
  data_files: 
  - split: test
    path: behavior-qa/test.jsonl
- config_name: judgment-qa
  data_files: 
  - split: test
    path: judgment-qa/test.jsonl
- config_name: story-data
  data_files: 
  - split: test
    path: story-data/test.jsonl
---
# SimpleToM Dataset and Evaluation data

The SimpleToM dataset of stories with associated questions are described in the paper 
["SimpleToM: Exposing the Gap between Explicit ToM Inference and Implicit ToM Application in LLMs"](https://arxiv.org/abs/2410.13648)

Associated evaluation data for the models analyzed in the paper can be found in the
separate dataset: [SimpleToM-eval-data](https://huggingface.co/datasets/SaveBertAndGpt/SimpleToM-eval-data).

## Question sets

There are three question sets in the SimpleToM dataset:

 * `mental-state-qa` questions about information awareness of character in the story
 * `behavior-qa` questions about likely future behavior of character in the story
 * `judgment-qa` questions about reasonableness of character's behavior

The questions follow a standard multiple-choice QA format, for instance:

```json
{
  "id":"gen1169_sev3_aware",
  "story":"Mike replaced the Oreo cookies in the package with dog treats that look similar to Oreos. Mike's friend spots the Oreo package on the kitchen table and reaches for it.",
  "question":"Is Mike's friend likely to be aware that \"Mike replaced the Oreo cookies in the package with dog treats that look similar to Oreos.\"?",
  "scenario_name":"inside_reuse_labeled_containers",
  "choices":{"text":["Yes","No"],"label":["A","B"]},
  "answerKey":"B"
}
```


## Story data

The `story-data/test.jsonl` file contains more detailed metadata about each story, including 
the original story prompt, the entities involved, the severity rating, and 
the predicted harmfulness and unethicality ratings.

Example story data with select comments:

```json
{
  "story_id":"gen1169_sev3",
  "core_id":"gen1169",
  "scenario_name":"inside_reuse_labeled_containers",
  "story_prompt_example":"gen168",  // Story used as prompt
  "entities":{"Person X":"Mike's friend","Person Y":"Mike","Object Z":"Oreo cookie package"},
  "severity_original":3,  // Original severity rating
  "harmfulness_predicted":[  // Harmfulness predictions
    {"harmfulness":3,"predictor_model":"claude-3-5-sonnet-20240620"},
    {"harmfulness":3,"predictor_model":"gpt-4o-2024-05-13"}
  ],
  "unethicality_predicted":[  // unethicality predictions
    {"unethicality":3,"predictor_model":"claude-3-5-sonnet-20240620"},
    {"unethicality":3,"predictor_model":"gpt-4o-2024-05-13"}
    ],
  "story":"Mike replaced the Oreo cookies in the package with dog treats that look similar to Oreos. Mike's friend spots the Oreo package on the kitchen table and reaches for it.",
  "key_information":"Mike replaced the Oreo cookies in the package with dog treats that look similar to Oreos.",
  "story_sentence":"Mike's friend spots the Oreo package on the kitchen table and reaches for it.",
  "story_generator_model":"claude-3-5-sonnet-20240620",  // Model used to generate story
  "questions":[
    {"question_id":"gen1169_sev3_aware",
      "question":"Is Mike's friend likely to be aware that \"Mike replaced the Oreo cookies in the package with dog treats that look similar to Oreos.\"?",
      "answer_correct":"No","answer_incorrect":"Yes"
    },
    {"question_id":"gen1169_sev3_action",
      "question":"What will Mike's friend likely do next?",
      "answer_correct":"Open the package and eat one of the cookies.",
      "answer_incorrect":"Express shock and concern about the potential health risks of eating dog treats."
    }
  ]
}
```


# Citation

```
@misc{gu2024simpletomexposinggapexplicit,
      title={SimpleToM: Exposing the Gap between Explicit ToM Inference and Implicit ToM Application in LLMs}, 
      author={Yuling Gu and Oyvind Tafjord and Hyunwoo Kim and Jared Moore and Ronan Le Bras and Peter Clark and Yejin Choi},
      year={2024},
      eprint={2410.13648},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2410.13648}, 
}
```
