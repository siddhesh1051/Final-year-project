from app.controllers import blueprint, mongo, jsonify, datetime, resnet, request
from app.schemas import validate_detectionHistory
from bson import ObjectId, json_util  # Correct import statement
import flask
from flask_cors import CORS, cross_origin

@blueprint.route('/api/dl', methods=["GET"])
def hello():
    return 'Hello, World!'

@blueprint.route('/api/dl/prediction/test', methods=['GET'])
def test1():
    print(ObjectId("623a3d74960a9f8526395e08"))
    data = validate_detectionHistory(
        {"createdAt": str(datetime.now()),
         "plantId": ObjectId("623a3d74960a9f8526395e08")})
    if data['ok']:
        data = data['data']
        print(mongo.db.detectionHistory.find_one())
        print(type(mongo.db.detectionHistory.find_one()['_id']))
        mongo.db.detectionHistory.insert_one(data)
        return jsonify({'ok': True, 'message': 'User created successfully!', 'detectionHistory': data}), 200

    return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

@blueprint.route('/api/dl/detection', methods=['POST'])
@cross_origin(supports_credentials=True)
def dl_detection():
    try:
        uid = '124352414'
        city = 'Mumbai'
        ip = '13143536'
        district = 'Mumbai City'
        state = 'MH'
        lat = 11.4652
        lon = 242.24

        image = request.files['image']
        detection = resnet.predict_image(image)
        print("detection", detection)
        detection_split = detection.split('___')
        plant, disease = detection_split[0], detection_split[1]
        print("plant", plant)
        print("disease", disease)
        disease_info = mongo.db.disease.find_one({"name": detection})
        print("disease_info", disease_info)
        plant_info = mongo.db.plants.find_one({"commonName" : plant})
        print("plant_info", plant_info)
        detectionHistory = {
            "createdAt": str(datetime.now()),
            "ip": ip,
            "city": city,
            "district": district,
            "state": state,
            "location": {
                "lat": lat,
                "lon": lon
            },
            "detected_class": detection,
            "plantId": str(plant_info['_id']),
            "diseaseId": str(ObjectId('507f191e810c19729de860ea')) if disease_info is None else str(disease_info['_id']),
            "rating": 5
        }

        validated_detectionHistory = validate_detectionHistory(detectionHistory)
        done = mongo.db.detectionHistory.insert_one(validated_detectionHistory['data'])
        response_data = {
            'ok': True,
            'detection': detection,
            'validated_detectionHistory': validated_detectionHistory,
            'plant': plant_info,
            'disease': "No disease found" if disease_info is None else disease_info
        }
        response = flask.jsonify(json_util.dumps(response_data))  # Use json_util for ObjectId serialization
        return response
    except Exception as ex:
        return flask.jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(ex)}), 500
