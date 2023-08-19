
prompt = """
You need to act as a policy model, that given a question and a modular set, determines the sequence of modules that can be executed sequentially can solve the question.

The modules are defined as follows:

- Calculate[formula]: This module calculates a given formula and returns the result. It takes in a mathematical formula and returns the calculated result. Normally, we only consider using "Calculate" when the question involves mathematical computations.

- RetrieveAgenda[keyword]: This module retrieves an agenda related to a specific keyword and returns it. It takes in a keyword and returns the corresponding agenda. Normally, we only consider using "RetrieveAgenda" when the question is about specific actions or tasks related to a topic.

- RetrieveScirex[keyword]: This module retrieves paragraphs from machine learning papers related to the specified keyword and returns them. It takes in a keyword and returns the relevant paragraphs. Normally, we only consider using "RetrieveScirex" when the question involves understanding specific concepts in machine learning.

- LoadDB[DBName]: This module loads a database specified by the database name and returns the loaded database. It takes in a database name and returns the corresponding database. The DBName can be one of the following: flights/coffee/airbnb/yelp. Normally, we only consider using "LoadDB" when the question requires data from a specific structured dataset.

- FilterDB[column_name, relation, value]: This module filters a database by a specified column name, relation, and value, and then returns the filtered database. It takes in a column name, a relation, and a value, and returns the filtered database. Normally, we only consider using "FilterDB" when the question requires a specific subset of data from a structured dataset.

- GetValue[column_name]: This module returns the value of a specified column in a database. It takes in a column name and returns its value. Normally, we only consider using "GetValue" when the question requires a specific piece of data from a structured dataset.

- LoadGraph[GraphName]: This module loads a graph specified by the graph name and returns the loaded graph. It takes in a graph name and returns the corresponding graph. Normally, we only consider using "LoadGraph" when the question involves understanding or navigating specific graph structures.

- NeighbourCheck[GraphName, Node]: This module lists the neighbors of a specified node in a graph and returns the neighbors. It takes in a graph name and a node, and returns the node's neighbors. Normally, we only consider using "NeighbourCheck" when the question involves understanding relationships in a graph structure.

- NodeCheck[GraphName, Node]: This module returns the detailed attribute information of a specified node in a graph. It takes in a graph name and a node, and returns the node's attributes. Normally, we only consider using "NodeCheck" when the question requires information about a specific entity in a graph.

- EdgeCheck[GraphName, Node1, Node2]: This module returns the detailed attribute information of the edge between two specified nodes in a graph. It takes in a graph name and two nodes, and returns the attributes of the edge between them. Normally, we only consider using "EdgeCheck" when the question involves understanding the relationship between two entities in a graph.

- SQLInterpreter[SQL]: This module interprets a SQL query and returns the result. It takes in a SQL query and returns the result of the query. Normally, we only consider using "SQLInterpreter" when the question requires data manipulation and extraction from a structured dataset.

- PythonInterpreter[Python]: This module interprets Python code and returns the result. It takes in Python code and returns the result of the code execution. Normally, we only consider using "PythonInterpreter" when the question requires complex computations or custom data manipulation.

- Finish[answer]: This module returns the final answer and finishes the task. This module is the final module in the sequence that encapsulates the result of all previous modules.

Below are some examples that map the problem to the modules.

Question: How many extra minutes did the DL1575 flight take from ATL to MCO on 2022-01-12?

Modules: ["LoadDB[flights]", "FilterDB[Flight_Number_Marketing_Airline=1575, FlightDate=2022-01-12, Origin=ATL, Dest=MCO]", "GetValue[DepDelay]", "GetValue[ArrDelay]", "Calculate[(-17)-(-7)]", "Finish[-10]"]

Question: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?

Modules: ["PythonInterpreter[# solution in Python:\n\ndef solution():\n # Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?\n golf_balls_initial = 58\n golf_balls_lost_tuesday = 23\n golf_balls_lost_wednesday = 2\n golf_balls_left = golf_balls_initial - golf_balls_lost_tuesday - golf_balls_lost_wednesday\n result = golf_balls_left\n return result]", "Finish[33]"]

Question: What is the corresponding Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task?

Modules: ["ScirexRetrieve[Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task]", "Finish[71.8%]"]

Question: When was the paper Learning the Principle of Least Action with Reinforcement Learning. published?

Modules: ["LoadGraph[dblp]", "NodeCheck[PaperNet, Learning the Principle of Least Action with Reinforcement Learning.]", "Finish[2021]"]

Question: How many collaborators does Chao Zhang have in the DBLP graph?

Modules: ["LoadGraph[dblp]", "NeighbourCheck[AuthorNet, Chao Zhang]", "Finish[6]"]

Question: How many papers does Chao Zhang and Weihong Lin have in common in the DBLP graph?

Modules: ["LoadGraph[dblp]", "EdgeCheck[PaperNet, Chao Zhang, Weihong Lin]", "Finish[1]"]

Question: Where did Stephen's Opera performance take place?

Modules: ["AgendaRetrieve[Stephen's Opera performance]", "Finish[Lyric Opera]"]

Question: What was the trading volume of coffee on 2000-01-14?

Modules: ["SQLInterpreter[SELECT Volume FROM coffee.coffee_data WHERE Date = '2000-01-14']", "Finish[10115]"]

Now, you need to act as a policy model, that given a question and a modular set, determines the sequence of modules that can be executed sequentially can solve the question.
"""



prompt_clean = """
You need to act as a policy model, that given a question and a modular set, determines the sequence of modules that can be executed sequentially can solve the question.

The modules are defined as follows:

- Calculate[formula]: This module calculates a given formula and returns the result. It takes in a mathematical formula and returns the calculated result. Normally, we only consider using "Calculate" when the question involves mathematical computations.

- RetrieveAgenda[keyword]: This module retrieves an agenda related to a specific keyword and returns it. It takes in a keyword and returns the corresponding agenda. Normally, we only consider using "RetrieveAgenda" when the question is about specific actions or tasks related to a topic.

- RetrieveScirex[keyword]: This module retrieves paragraphs from machine learning papers related to the specified keyword and returns them. It takes in a keyword and returns the relevant paragraphs. Normally, we only consider using "RetrieveScirex" when the question involves understanding specific concepts in machine learning.

- LoadDB[DBName]: This module loads a database specified by the database name and returns the loaded database. It takes in a database name and returns the corresponding database. The DBName can be one of the following: flights/coffee/airbnb/yelp. Normally, we only consider using "LoadDB" when the question requires data from a specific structured dataset.

- FilterDB[column_name, relation, value]: This module filters a database by a specified column name, relation, and value, and then returns the filtered database. It takes in a column name, a relation, and a value, and returns the filtered database. Normally, we only consider using "FilterDB" when the question requires a specific subset of data from a structured dataset.

- GetValue[column_name]: This module returns the value of a specified column in a database. It takes in a column name and returns its value. Normally, we only consider using "GetValue" when the question requires a specific piece of data from a structured dataset.

- LoadGraph[GraphName]: This module loads a graph specified by the graph name and returns the loaded graph. It takes in a graph name and returns the corresponding graph. Normally, we only consider using "LoadGraph" when the question involves understanding or navigating specific graph structures.

- NeighbourCheck[GraphName, Node]: This module lists the neighbors of a specified node in a graph and returns the neighbors. It takes in a graph name and a node, and returns the node's neighbors. Normally, we only consider using "NeighbourCheck" when the question involves understanding relationships in a graph structure.

- NodeCheck[GraphName, Node]: This module returns the detailed attribute information of a specified node in a graph. It takes in a graph name and a node, and returns the node's attributes. Normally, we only consider using "NodeCheck" when the question requires information about a specific entity in a graph.

- EdgeCheck[GraphName, Node1, Node2]: This module returns the detailed attribute information of the edge between two specified nodes in a graph. It takes in a graph name and two nodes, and returns the attributes of the edge between them. Normally, we only consider using "EdgeCheck" when the question involves understanding the relationship between two entities in a graph.

- SQLInterpreter[SQL]: This module interprets a SQL query and returns the result. It takes in a SQL query and returns the result of the query. Normally, we only consider using "SQLInterpreter" when the question requires data manipulation and extraction from a structured dataset.

- PythonInterpreter[Python]: This module interprets Python code and returns the result. It takes in Python code and returns the result of the code execution. Normally, we only consider using "PythonInterpreter" when the question requires complex computations or custom data manipulation.

- Finish[answer]: This module returns the final answer and finishes the task. This module is the final module in the sequence that encapsulates the result of all previous modules.

Below are some examples that map the problem to the modules.

Question: How many extra minutes did the DL1575 flight take from ATL to MCO on 2022-01-12?

Modules: ["LoadDB", "FilterDB", "GetValue", "GetValue", "Calculate", "Finish"]

Question: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?

Modules: ["PythonInterpreter", "Finish"]

Question: What is the corresponding Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task?

Modules: ["ScirexRetrieve", "Finish"]

Question: When was the paper Learning the Principle of Least Action with Reinforcement Learning. published?

Modules: ["LoadGraph", "NodeCheck", "Finish"]

Question: How many collaborators does Chao Zhang have in the DBLP graph?

Modules: ["LoadGraph", "NeighbourCheck", "Finish"]

Question: How many papers does Chao Zhang and Weihong Lin have in common in the DBLP graph?

Modules: ["LoadGraph", "EdgeCheck", "Finish"]

Question: Where did Stephen's Opera performance take place?

Modules: ["AgendaRetrieve", "Finish"]

Question: What was the trading volume of coffee on 2000-01-14?

Modules: ["SQLInterpreter", "Finish"]

Now, you need to act as a policy model, that given a question and a modular set, determines the sequence of modules that can be executed sequentially can solve the question.
"""
