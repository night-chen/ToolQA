<div align= "center">
    <h1> 🛠️ToolQA</h1>
</div>

🛠️ The official repository for code and data of ToolQA dataset. ToolQA is a open-source dataset specifically designed for evaluations on tool-augmented large language models (LLMs). We provide the dataset, the corresponding data generation code, and the implementations of baselines on our dataset.

### Features
- Our questions are selected and guaranteed that **LLMs have little chance to memorize and answer correctly within their internal knowledge**;
- The majority of the questions in ToolQA **require compositional use of multiple tools**. According to the length of toolchains, we offer two different difficult levels of dataset: **Easy** and **Hard**.
- We apply **a thorough diagnosis and analysis of in-context tool-augmented LLMs** in our paper.
- ToolQA is **a human-AI collaborated dataset** that can automatically be applied on the other new data and questions.

<p align="center">
  <img 
    width="800"
    src="./figure/overview.png"
  >
</p>

### Generate New Questions
You can also use the ToolQA to generate new questions under our templates for tuning and new sets of evalations. We offer the data generation code in `/dataset_generation/` directory. The only thing to do is to modify the paths in the notebooks.


### Current Progress
The data and code are in the final stage of clean and will be public gradually in a very short period. We offer the detailed progress of the final examination in the TODO list part.

### To Do List -- Easy Questions
- [x] ~~Flight-easy questions and code;~~
- [ ] Coffee-easy questions and code;
- [ ] Yelp-easy questions and code;
- [ ] Airbnb-easy questions and code;
- [ ] SciREX-easy questions and code;
- [ ] Agenda-easy questions and code;
- [ ] GSM8K-easy questions and code;
- [ ] DBLP-easy questions and code;

### To Do List -- Hard Questions
- [ ] Flight-hard questions and code;
- [ ] Coffee-hard questions and code;
- [ ] Yelp-hard questions and code;
- [ ] Airbnb-hard questions and code;
- [ ] SciREX-hard questions and code;
- [ ] Agenda-hard questions and code;
- [ ] GSM8K-hard questions and code;
- [ ] DBLP-hard questions and code;

### Benchmark Code Release
- [ ] ChatGPT Vanilla;
- [ ] Chain-of-Thoughts;
- [ ] ReAct;
- [ ] Chameleon;

