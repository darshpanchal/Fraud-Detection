# Credit Card Fraud Detection

### Technology used:
- Flask
- Scikit-Learn
- Pandas
- NumPy
- Imbalanced-learn
- Kafka

### Files:
- backend.py does actual inference and returns prediction over kafka topic.
- flaskapi.py is a forefront for accepting api calls over POST and sending it to backend via kafka topics.
- testapi.py mimics a demo api call using requests library.

### Explanation and Working:
- This repo focuses more on scalability, thus it uses kafka for streaming.
1. A user sends POST request to flaskapi endpoint containing transaction information and a unique id for request identification.
2. flaskapi receives inputdata and then sends it to a kafka topic (fraudsender) and waits for response by backend on kafka topic (fraudreceiver).
3. backend receives data over fraudsender topic and runs model inference on transaction information. After inference, it sends prediction and id over fraudreceiver topic.
4. After receiving prediction msg over fraudreceiver topic, flaskapi responds user with prediction.

### Dataset information:
- Model uses creditcard dataset from kaggle.

### Model info:
- I used SMOTE as this dataset is highly imbalanced.
- Used Randomforest (with standardscaler in pipeline) on first 20000 rows with accuracy of 99%.
- I haven't included model training script, contact me over email if you need.

### Upgrades:
- Using database like Cassandra or MongoDB for storing main database and prediction database.
- Using docker for backend.

PS- Will make a tutorial blog soon..