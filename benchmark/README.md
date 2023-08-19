<div align= "center">
    <h1> 🛠️ToolQA</h1>
</div>

🛠️ The benchmark code of **ToolQA** dataset. ToolQA is a open-source dataset specifically designed for evaluations on tool-augmented large language models (LLMs). This repo provides the dataset, the corresponding data generation code, and the implementations of baselines on our dataset.

## Methods
Below are the methods implemented on ToolQA for performance evaluation and comparison:

### ChatGPT
We directly feed the question into OpenAI’s ChatGPT model (gpt-3.5-turbo) and obtain its response as the final answer. Please run the scripts under the ``./scripts/run_chatgpt.sh`` directory.

### ReAct
ReAct integrates reasoning with tool use by prompting LLMs to generate interleaved verbal reasoning traces and tool calls. This integration has been shown effective in enhancing LLMs’ problem-solving capabilities. We instantiate two versions of ReAct using gpt-3.5-turbo and text-davinci-003. The implementation is modified from the [official repository of Reflexion](https://github.com/noahshinn024/reflexion). Please run the scripts under the ``./scripts/run_react.sh`` directory.

### Chameleon
Chameleon is a recent method that uses LLMs as a controller to use multiple tools for solving subtasks and has shown promising results in reasoning and QA tasks. We modify the code from the [official repo](https://github.com/lupantech/chameleon-llm) and change the tool set into our own tools. Please run the scripts under the ``./scripts/run_chameleon.sh`` directory.

### LLaMA-2
LLaMA-2 is the most recent open-source LLMs, we also test its ability to answer all the questions. Please run the scripts under the ``./scripts/run_llama.sh`` directory.

## Model Performances
Model performances on the easy questions of ToolQA:
| Easy            | Flight | Coffee | Agenda | Yelp | DBLP | GSM8K | SciREX | Airbnb | Average |
|:-----------------|:------:|:------:|:------:|:----:|:----:|:-----:|:------:|:------:|:-------:|
| ChatGPT         |   2.0  |   0.0  |   0.0  | 15.0 |  0.0 |  2.0  |  26.0  |   0.0  |   5.6   |
| LLaMA-2 (13B)   |   0.0  |   2.0  |   0.0  |  5.0 |  1.0 |  0.0  |   9.0  |   1.0  |   2.3   |
| CoT             |   1.0  |   1.0  |   0.0  |  9.0 |  0.0 |  0.0  |  30.0  |   0.0  |   5.1   |
| Chameleon       |  30.0  |   9.0  |   4.0  |  8.0 |  3.0 |  0.0  |  27.0  |   4.0  |   10.6  |
| ReAct (GPT-3)   |  61.0  |  90.0  |  29.0  | 77.0 | 28.0 |  3.0  |  32.0  |  25.0  |   43.1  |
| ReAct (GPT-3.5) |  48.0  |  81.0  |  24.0  | 64.0 | 23.0 |  2.0  |  23.0  |  29.0  |   36.8  |

Model performances on the hard questions of ToolQA:
| Hard            | Flight | Coffee | Agenda | Yelp | DBLP | SciREX | Airbnb | Average |
|-----------------|:------:|:------:|:------:|:----:|:----:|:------:|:------:|:-------:|
| ChatGPT         |   2.0  |   2.3  |   1.0  |  0.0 |  2.0 |   4.0  |   3.0  |   2.0   |
| LLaMA-2 (13B)   |   1.0  |   0.0  |   0.0  |  4.0 |  1.0 |   5.0  |   1.0  |   1.7   |
| CoT             |   0.0  |   0.8  |   0.0  |  1.0 |  0.0 |   3.0  |   5.0  |   1.4   |
| Chameleon       |   3.0  |   2.3  |   0.0  |  0.0 |  0.0 |   8.0  |   0.0  |   1.9   |
| ReAct (GPT-3)   |   3.0  |  10.8  |   0.0  |  3.0 |  0.0 |  19.0  |   0.0  |   5.1   |
| ReAct (GPT-3.5) |   5.0  |  17.7  |   7.0  |  8.0 |  7.0 |   5.0  |   8.0  |   8.2   |

## Citation
If you find this repository valuable for your research, we kindly request that you acknowledge our paper by citing the following paper. We appreciate your consideration.

```
@misc{zhuang2023toolqa,
      title={ToolQA: A Dataset for LLM Question Answering with External Tools}, 
      author={Yuchen Zhuang and Yue Yu and Kuan Wang and Haotian Sun and Chao Zhang},
      year={2023},
      eprint={2306.13304},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}

@article{lu2023chameleon,
  title={Chameleon: Plug-and-Play Compositional Reasoning with Large Language Models},
  author={Lu, Pan and Peng, Baolin and Cheng, Hao and Galley, Michel and Chang, Kai-Wei and Wu, Ying Nian and Zhu, Song-Chun and Gao, Jianfeng},
  journal={arXiv preprint arXiv:2304.09842},
  year={2023}
}

@misc{shinn2023reflexion,
      title={Reflexion: Language Agents with Verbal Reinforcement Learning}, 
      author={Noah Shinn and Federico Cassano and Beck Labash and Ashwin Gopinath and Karthik Narasimhan and Shunyu Yao},
      year={2023},
      eprint={2303.11366},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}

@article{yao2022react,
  title={ReAct: Synergizing Reasoning and Acting in Language Models},
  author={Yao, Shunyu and Zhao, Jeffrey and Yu, Dian and Du, Nan and Shafran, Izhak and Narasimhan, Karthik and Cao, Yuan},
  journal={arXiv preprint arXiv:2210.03629},
  year={2022}
}
```
