import os
import flask
import sys

def serve_local_model():
  sys.path.insert(0, os.getcwd())
  # check that files exist
  print('> Loading predictor.py...')
  try:
    from predictor import Predictor
  except Exception as e:
    print('> Errror! Could not load predictor.py:')
    print(str(e))
    exit()

  print('> predictor.py loaded correctly.')
  loaded_predictor = Predictor()

  try:
    print('> Calling predictor.load()')
    loaded_predictor.load()
  except Exception as e:
      print('> Error! An error occurred while loading your model with Preditor.load:')
      print(str(e))
      sys.exit()

  print('> predictor.load() ran successfully')
  # instantiate flask
  app = flask.Flask(__name__)

  @app.route('/', methods=['POST'])
  def predict():
    data = {"success": False}
    body = flask.request.json
    print('> Request coming in. Body is:')
    print(body)
    
    try:
      data = loaded_predictor.predict(body)
    except Exception as e:
      data["message"] = "There was an error while running your model: " + str(e)

    return flask.jsonify(data)

  # start the flask app, allow remote connections
  print('> Local server is running on port 3009')
  app.run(host='0.0.0.0', port=3009)