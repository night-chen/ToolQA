TOOLQA_EASY8 = """Question: How many extra minutes did the DL1575 flight take from ATL to MCO on 2022-01-12?
Thought 1: This is a question related to flights. We need to load the flights database.
Action 1: LoadDB[flights]
Observation 1: We have successfully loaded the flights database, including the following columns: FlightDate, Airline, Origin, Dest, Cancelled, Diverted, CRSDepTime, DepTime, DepDelayMinutes, DepDelay, ArrTime, ArrDelayMinutes, AirTime, CRSElapsedTime, ActualElapsedTime, Distance, Year, Quarter, Month, DayofMonth, DayOfWeek, Marketing_Airline_Network, Operated_or_Branded_Code_Share_Partners, DOT_ID_Marketing_Airline, IATA_Code_Marketing_Airline, Flight_Number_Marketing_Airline, Operating_Airline, DOT_ID_Operating_Airline, IATA_Code_Operating_Airline, Tail_Number, Flight_Number_Operating_Airline, OriginAirportID, OriginAirportSeqID, OriginCityMarketID, OriginCityName, OriginState, OriginStateFips, OriginStateName, OriginWac, DestAirportID, DestAirportSeqID, DestCityMarketID, DestCityName, DestState, DestStateFips, DestStateName, DestWac, DepDel15, DepartureDelayGroups, DepTimeBlk, TaxiOut, WheelsOff, WheelsOn, TaxiIn, CRSArrTime, ArrDelay, ArrDel15, ArrivalDelayGroups, ArrTimeBlk, DistanceGroup, DivAirportLandings
Thought 2: We need to filter the information related to the query.
Action 2: FilterDB[Flight_Number_Marketing_Airline=1575, FlightDate=2022-01-12, Origin=ATL, Dest=MCO]
Observation 2: We have successfully filtered the data (1 row).
Thought 3: We then need to know the departure delayed time.
Action 3: GetValue[DepDelay]
Observation 3: -7.0
Thought 4: We then need to know the arrival delayed time.
Action 4: GetValue[ArrDelay]
Observation 4: -17.0
Thought 5: To compute the extra minutes, we need to subtract the departure delayed time from the arrival delayed time.
Action 5: Calculate[(-17)-(-7)]
Observation 5: -10
Thought 6: After calculation, we know that the answer is -10.
Action 6: Finish[-10]

Question: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?
Thought 1: Maybe I can write a python program to solve this problem.
Action 1: PythonInterpreter[# solution in Python:
def solution():
    # Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?
    golf_balls_initial = 58
    golf_balls_lost_tuesday = 23
    golf_balls_lost_wednesday = 2
    golf_balls_left = golf_balls_initial - golf_balls_lost_tuesday - golf_balls_lost_wednesday
    result = golf_balls_left
    return result]
Observation 1: 33
Thought 2: After execution of Python Code, we know that the answer is 33.
Action 2: Finish[33]

Question: What is the corresponding Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task?
Thought 1: The question is asking some performance information about Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task, we need to retrieve some useful information from the scirex database.
Action 1: RetrieveScirex[Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task]
Observation 1: section : Abstract Semantic image segmentation is an essential component of modern autonomous driving systems , as an accurate understanding of the surrounding scene is crucial to navigation and action planning . Current state - of - the - art approaches in semantic image segmentation rely on pretrained networks that were initially developed for classifying images as a whole . While these networks exhibit outstanding recognition performance ( i.e. , what is visible ? ) , they lack localization accuracy ( i.e. , where precisely is something located ? ) . Therefore , additional processing steps have to be performed in order to obtain pixel - accurate segmentation masks at the full image resolution . To alleviate this problem we propose a novel ResNet - like architecture that exhibits strong localization and recognition performance . We combine multi - scale context with pixel - level accuracy by using two processing streams within our network : One stream carries information at the full image resolution , enabling precise adherence to segment boundaries . The other stream undergoes a sequence of pooling operations to obtain robust features for recognition . The two streams are coupled at the full image resolution using residuals . Without additional processing steps and without pretraining , our approach achieves an intersection - over - union score of 71.8 % on the Cityscapes dataset .
Thought 2: As the approach achieves an intersection - over - union score of 71.8 % on the Cityscapes dataset, the answer should be 71.8%.
Action 2: Finish[71.8%]

Question: When was the paper Learning the Principle of Least Action with Reinforcement Learning. published?
Thought 1: The question is asking some basic information of a dblp paper. We need to load the DBLP graph.
Action 1: LoadGraph[dblp]
Observation 1: DBLP graph is loaded.
Thought 2: The question is asking the published date of a paper, we need to check the node from the PaperNet in DBLP graph.
Action 2: NodeCheck[PaperNet, Learning the Principle of Least Action with Reinforcement Learning.]
Observation 2: {'title': 'Learning the Principle of Least Action with Reinforcement Learning.', 'year': 2021, 'venue': {'raw': 'AAAI Spring Symposium - MLPS'}, 'n_citation': 0, 'keywords': [], 'doc_type': 'Conference', 'page_start': '', 'page_end': ''}
Thought 3: The published date of the paper is 2021.
Action 3: Finish[2021]

Question: How many collaborators does Chao Zhang have in the DBLP graph?
Thought 1: The question is asking the number of collaborators of a person, we need load the DBLP graph.
Action 1: LoadGraph[dblp]
Observation 1: DBLP graph is loaded.
Thought 2: The question is asking the collaborators of a person, we need to check the neighboring nodes from the AuthorNet in DBLP graph.
Action 2: NeighbourCheck[AuthorNet, Chao Zhang]
Observation 2: ['YUHUI YUAN', 'Rao Fu', 'Lang Huang', 'Weihong Lin', 'X Chen', 'Jingdong Wang']
Thought 3: The number of collaborators of Chao Zhang is 6.
Action 3: Finish[6]

Question: How many papers does Chao Zhang and Weihong Lin have in common in the DBLP graph?
Thought 1: The question is asking the number of common papers of two persons, we need load the DBLP graph.
Action 1: LoadGraph[dblp]
Observation 1: DBLP graph is loaded.
Thought 2: The question is asking the common papers of two persons, we need to check the edges between them from the PaperNet in DBLP graph.
Action 2: EdgeCheck[PaperNet, Chao Zhang, Weihong Lin]
Observation 2: {'weight': 1, 'papers': ['HRFormer: High-Resolution Vision Transformer for Dense Predict.'], 'n_citation': [95]}
Thought 3: The number of common papers of Chao Zhang and Weihong Lin is 1.

Question: Where did Stephen's Opera performance take place?
Thought 1: The question is asking the location of Stephen's Opera performance from agenda.
Action 1: RetrieveAgenda[Stephen's Opera performance]
Observation 1: On January 29, 2022, there will be an opera performance at the Lyric Opera House, featuring Stephen. The show will start at 7:00 PM and end at 9:00 PM. It promises to be a wonderful evening of beautiful music and powerful performances in a stunning venue. Come and experience the magic of opera at its finest!
Thought 2: The event happened in Lyric Opera.
Action 2: Finish[Lyric Opera]

Question: What was the trading volume of coffee on 2000-01-14?
Thought 1: Maybe I can write a SQL query to solve this problem.
Action 1: SQLInterpreter(SELECT Volume FROM coffee.coffee_data WHERE Date = '2000-01-14';
Observation 1: Volume: 10115
Thought 2: The volume of coffee on 2000-01-14 is 10115.
Action 2: Finish[10115]
"""

TOOLQA_HARD3 = """Question: What is the average airtime of the flights from PHX to LGA host by Spirit Air Lines?
Thought 1: This is a question related to flights. We need to load the flights database.
Action 1: LoadDB[flights]
Observation 1: We have successfully loaded the flights database, including the following columns: FlightDate, Airline, Origin, Dest, Cancelled, Diverted, CRSDepTime, DepTime, DepDelayMinutes, DepDelay, ArrTime, ArrDelayMinutes, AirTime, CRSElapsedTime, ActualElapsedTime, Distance, Year, Quarter, Month, DayofMonth, DayOfWeek, Marketing_Airline_Network, Operated_or_Branded_Code_Share_Partners, DOT_ID_Marketing_Airline, IATA_Code_Marketing_Airline, Flight_Number_Marketing_Airline, Operating_Airline, DOT_ID_Operating_Airline, IATA_Code_Operating_Airline, Tail_Number, Flight_Number_Operating_Airline, OriginAirportID, OriginAirportSeqID, OriginCityMarketID, OriginCityName, OriginState, OriginStateFips, OriginStateName, OriginWac, DestAirportID, DestAirportSeqID, DestCityMarketID, DestCityName, DestState, DestStateFips, DestStateName, DestWac, DepDel15, DepartureDelayGroups, DepTimeBlk, TaxiOut, WheelsOff, WheelsOn, TaxiIn, CRSArrTime, ArrDelay, ArrDel15, ArrivalDelayGroups, ArrTimeBlk, DistanceGroup, DivAirportLandings
Thought 2: We need to filter the information related to the query.
Action 2: FilterDB[Origin=PHX, Dest=ATL, Airline=Spirit Air Lines]
Observation 2: We have successfully filtered the data (16 rows).
Thought 2: We then obtain all the AirTime values of filtered records.
Action 2: GetValue[AirTime]
Observation 2: [247.0, 253.0, 230.0, 264.0, 254.0, 275.0, 227.0, 258.0, 245.0, 253.0, 242.0, nan, 229.0, nan, 259.0, 253.0]
Thought 3: We then calculate the average of the values. NaN values are ignored.
Action 3: Calculate(mean(247.0, 253.0, 230.0, 264.0, 254.0, 275.0, 227.0, 258.0, 245.0, 253.0, 242.0, 229.0, 259.0, 253.0))
Observation 3: 249.214
Thought 4: The average airtime of the flights from PHX to LGA host by Spirit Air Lines is 249.2.
Action 4: Finish[249.2]

Question: Can you recommend a Guamanian business with the highest star rating within a 5-mile radius of 6830 Rising Sun Ave?
Thought 1: This is a question related to business. We need to load the yelp database.
Action 1: LoadDB[yelp]
Observation 1: We have successfully loaded the yelp database, including the following columns: business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open, attributes, categories, hours
Thought 2: Maybe we can write SQL code to obtain the latitude and longitude of the address.
Action 2: SQLInterpreter[SELECT latitude, longitude FROM yelp.yelp_data WHERE address='6830 Rising Sun Ave']  
Observation 2: latitude: 40.05555, longitude: -75.090723 
Thought 3: Maybe we can write another python code to calculate the coordinates range of 5-mile radius.
Action 3: import geopy\nimport geopy.distance\nlatitude = 40.05555\nlongitude = -75.090723\n_, lo_max, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=90)\n_, lo_min, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=270)\nla_max, _, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=0)\nla_min, _, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=180)\nans = (la_max, la_min, lo_max, lo_min)
Observation 3: (40.10058038657396, 40.010519262352226, -75.03212327463275, -75.14932272536724)
Thought 4: We then filter the information related to the query in the yelp database.
Action 4: FilterDB[latitude>=40.010519262352226, longitude>=-75.14932272536724, latitude<=40.10058038657396, longitude<=-75.03212327463275, categories=Guamanian]
Observation 4: We have successfully filtered the data (2 rows).
Thought 5: We then obtain all the stars values of filtered records.
Action 5: GetValue[stars]
Observation 5: [4.0, 4.5]
Thought 6: The highest star rating is 4.5. Select the business with the highest star rating.
Action 6: FilterDB[stars=4.5]
Observation 6: We have successfully filtered the data (1 row).
Thought 7: Get the corresponding name.
Action 7: GetValue[name]
Observation 7: Damaso Painting
Thought 8: The business with the highest star rating is Damaso Painting.
Action 8: Finish[Damaso Painting]

Question: What venue does Chao Zhang with his collarborator publish paper on?
Thought 1: This is a question related to DBLP. We need to load the DBLP graph.
Action 1: LoadGraph[dblp]
Observation 1: DBLP graph is loaded.
Thought 2: We need to check the neighbouring nodes of Chao Zhang in AuthorNet.
Action 2: NeighbourCheck[AuthorNet, Chao Zhang]
Observation 2: Weihong Lin
Thought 3: We need to check the between Chao Zhang and Weihong Lin to check their collaboration.
Action 3: EdgeCheck[AuthorNet, Chao Zhang, Weihong Lin]
Observation 3: {'weight': 1, 'papers': ['HRFormer: High-Resolution Vision Transformer for Dense Predict.'], 'n_citation': [95]}
Thought 4: We need to check the paper detail in the node feature from PaperNet they published.
Action 4: NodeCheck[PaperNet, HRFormer: High-Resolution Vision Transformer for Dense Predict.]
Observation 4: {'title': 'HRFormer: High-Resolution Vision Transformer for Dense Predict.', 'year': 2021, 'venue': {'raw': 'AAAI Spring Symposium - MLPS'}, 'n_citation': 0, 'keywords': [], 'doc_type': 'Conference', 'page_start': '', 'page_end': ''}
Thought 5: The paper is published on AAAI Spring Symposium - MLPS.
Action 5: Finish[AAAI Spring Symposium - MLPS]
"""
COTQA_SIMPLE6 = """Question: How many extra minutes did the DL1575 flight take from ATL to MCO on 2022-01-12?
Let's think step by step. I need to first load the flights database with LoadDB[flights]. And then, I need to filter the information I want according to the query with FilterDB[Flight_Number_Marketing_Airline=1575, FlightDate=2022-01-12, Origin=ATL, Dest=MCO]. Then, I need to get the value of the departure time from the database with GetValue[DepDelay]. We then need to know the arrival delayed time with GetValue[ArrDelay]. To compute the extra minutes, we need to subtract the departure delayed time from the arrival delayed time with Calculate[(-17)-(-7)].  After calculation, we know that the answer is -10.
Action 1: LoadDB[flights]-->FilterDB[Flight_Number_Marketing_Airline=1575, FlightDate=2022-01-12, Origin=ATL, Dest=MCO]-->GetValue[DepDelay]-->GetValue[ArrDelay]-->Calculate[(-17)-(-7)]-->Finish[-10]
"""
COT = """
"""

COT_REFLECT = """
"""

REFLECTIONS = """
"""