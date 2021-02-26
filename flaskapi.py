from kafka import KafkaConsumer, KafkaProducer
from flask import Flask, jsonify, request
import json
app = Flask(__name__)

@app.route('/predict', methods=['POST']) # api route and only POST is accepted
def predict():
    # create a kafka producer to send data to backend for processing.
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda m: json.dumps(m).encode('ascii'))
    # create a kafka consumer which receives msgs from backend to send back to user
    consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         consumer_timeout_ms=1000, value_deserializer=lambda m: json.loads(m.decode('ascii')))
    consumer.subscribe(['fraudreceiver']) # subscribing to fraudreceiver topic to receive updates
    
    inputdata = request.json # gets data from post request sent by user.
    cid = inputdata['id'] # gets randomly generated uuid from request
    print(cid)
    producer.send('fraudsender', inputdata) # sends inputdata to backend using fraudsender topic
    
    for msg in consumer: # checks for new msgs in topic
        if msg.value['id'] == cid: #only sends if id is matched so that only request sent by user is received
            result = msg.value
        else:
            continue

    return jsonify(result) # returns results in json format
        

if __name__ == '__main__':
    app.run(debug=True, threaded=True) # runs a dev server with multithreading enabled.
