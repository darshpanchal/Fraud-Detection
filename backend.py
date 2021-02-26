import logging, time
import json
from kafka import KafkaConsumer, KafkaProducer
import joblib
import pandas as pd

class BackEnd():
    def __init__(self):
        self.model = joblib.load('model0.pipeline') # load model
        
    def runprocess(self):
        # create a kafka consumer which receives msgs from flaskapi to process
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000, value_deserializer=lambda m: json.loads(m.decode('ascii'))) 
        consumer.subscribe(['fraudsender']) # subscribing to fraudsender topic to receive updates
        # create a kafka producer to send computed predictions back to flaskapi which sends to user.
        producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda m: json.dumps(m).encode('ascii'))

        while True: # runs forever checking for updates in msgs from consumer
            for message in consumer:
                df = pd.DataFrame.from_records([message.value]) # creates a pandas dataframe from received data
                cid = message.value['id'] # gets generated uuid from user
                print(cid)
                df = df.drop(['Time','id'],axis=1) # drops irrelavant columns from dataframe for inference
                pred = self.model.best_estimator_.predict(df)[0] # predict function
                producer.send('fraudreceiver', {'id': cid, 'result': int(pred)}) # sends prediction back to flaskapi using fraudreceiver topic

        consumer.close()
        producer.close()
        
    
        
if __name__ == "__main__":
    c = BackEnd()
    c.runprocess()
    logging.basicConfig(
        format='%(asctime)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )