from plant import *
from flask import Flask, Blueprint, render_template, request, jsonify
from swagger_ui_bundle import swagger_ui_path
from flask_cors import cross_origin
from flask_swagger import swagger

import os
application = Flask(__name__, static_url_path='', template_folder=".")
api = Blueprint('ballonplate', __name__)
swaggerapi = Blueprint('swagger_ui', __name__, static_url_path='',
                       static_folder=swagger_ui_path, template_folder=swagger_ui_path)

SWAGGER_UI_CONFIG = {
    "openapi_spec_url": "/spec"
}


object_detection_data = {}


@swaggerapi.route('/')
def swagger_ui_index():
    return render_template('index.j2', **SWAGGER_UI_CONFIG)


@application.route("/spec")
def spec():
    swag = swagger(application)
    swag['info']['version'] = "0.1"
    swag['info']['title'] = "Differential Drive Velocity API"
    return jsonify(swag)


@api.route('/stop', methods=['GET'])
@cross_origin()
def close():
    """
    Stop the system.
    ---
    responses:
        200:
            description: Valid response from server (contains payload with actual status).
        404:
            description: Not Found.
        405:
            description: Method not allowed.
    """
    return exit(0)


@api.route('/<int:idx>/', methods=['GET'])
@api.route('/<int:idx>/index.html', methods=['GET'])
@cross_origin(idx=0)
def index(idx=0):
    """
    Provides access to a view of the system.
    ---
    parameters:
      - name: idx
        in: path
        type: string
        required: true
        description: The id of the relevant sub-system
    responses:
        200:
            description: Valid response from server (contains payload with actual status).
        404:
            description: Not Found.
        405:
            description: Method not allowed.
    """
    return render_template('index2.html', idx=idx)


@api.route('/<int:idx>/3', methods=['GET'])
@cross_origin(idx=0)
def index3(idx=0):
    """
    Provides access to a view of the system.
    ---
    parameters:
      - name: idx
        in: path
        type: string
        required: true
        description: The id of the relevant sub-system
    responses:
        200:
            description: Valid response from server (contains payload with actual status).
        404:
            description: Not Found.
        405:
            description: Method not allowed.
    """
    return render_template('index3.html', idx=idx)


@api.route('/<int:idx>/init', methods=['GET'])
@cross_origin()
def initservice(idx=0):
    """
    Initializes the state of the system
    ---
    parameters:
      - name: idx
        in: path
        type: string
        required: true
        description: The id of the relevant sub-system
      - in: query
        name: value0
        type: string
        description: The position of the robot in x-axis
      - in: query
        name: value1
        type: string
        description: The position of the robot in y-axis
      - in: query
        name: t0
        type: string
        description: The time the robot is initialised
    responses:
        200:
            description: Valid response from server (contains payload with actual status).
        404:
            description: Not Found.
        405:
            description: Method not allowed.
    """
    f = init(request.full_path, idx)
    return f


@api.route('/<int:idx>/state', methods=['GET'])
@cross_origin()
def getstate(idx=None):
    """
    Returns the state of the system
    ---
    parameters:
      - name: idx
        in: path
        type: string
        required: true
        description: The id of the relevant sub-system
    responses:
        200:
            description: Valid response from server (contains payload with actual status).
        404:
            description: Not Found.
        405:
            description: Method not allowed.
    """
    f = state(idx)
    return f


@api.route('/<int:idx>/object-detection', methods=['POST'])
@cross_origin()
def receive_object_data(idx):
    """
    Receives object detection results for a specific subsystem.
    ---
    parameters:
      - name: idx
        in: path
        type: integer
        required: true
        description: The ID of the relevant sub-system.
      - in: body
        name: body
        schema:
          type: object
          properties:
            timestamp:
              type: string
              description: The time the detection was made.
            detections:
              type: array
              description: A list of detected objects.
              items:
                type: object
                properties:
                  class:
                    type: string
                    description: The name of the detected object.
                  score:
                    type: number
                    format: float
                    description: The confidence score of the detection.
                  bbox:
                    type: array
                    items:
                      type: number
                      format: float
                    description: The bounding box [x, y, width, height] of the object.
    responses:
      200:
        description: Object data received successfully.
      400:
        description: Invalid request body.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        # Store the data using the subsystem index (idx) as the key.
        object_detection_data[idx] = data

        return jsonify({"message": f"Data for subsystem {idx} received successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api.route('/<int:idx>/object-detection', methods=['GET'])
@cross_origin()
def get_object_data(idx):
    """
    Exposes the most recent object detection results for a specific subsystem.
    ---
    parameters:
      - name: idx
        in: path
        type: integer
        required: true
        description: The ID of the relevant sub-system.
    responses:
      200:
        description: Returns the latest object detection data.
        schema:
          type: object
          properties:
            timestamp:
              type: string
              description: The time the detection was made.
            detections:
              type: array
              description: A list of detected objects.
              items:
                type: object
                properties:
                  class:
                    type: string
                    description: The name of the detected object.
                  score:
                    type: number
                    format: float
                    description: The confidence score of the detection.
                  bbox:
                    type: array
                    items:
                      type: number
                      format: float
                    description: The bounding box [x, y, width, height] of the object.
      404:
        description: No object data available for this subsystem.
    """
    # Retrieve data using the subsystem index (idx).
    data = object_detection_data.get(idx)
    
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"message": f"No object data available for subsystem {idx}"}), 404


@api.route('/<int:idx>/u', methods=['GET'])
@cross_origin()
def model(idx=0):
    """
    Controls the state of the system
    ---
    parameters:
      - name: idx
        in: path
        type: string
        required: true
        description: The id of the relevant sub-system
      - in: query
        name: value0
        type: string
        description: The first value
      - in: query
        name: value1
        type: string
        description: The second value
      - in: query
        name: time
        type: number
        description: The time in milliseconds the control value was assigned
    responses:
        200:
            description: Valid response from server (contains payload with actual status).
        404:
            description: Not Found.
        405:
            description: Method not allowed.
    """

    f = interpret(request.full_path, idx)
    return f


application.register_blueprint(api)
application.register_blueprint(swaggerapi, url_prefix="/ui")

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8080))
    application.run(host='0.0.0.0', port=port)
