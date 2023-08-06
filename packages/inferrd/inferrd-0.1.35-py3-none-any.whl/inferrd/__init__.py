import requests
import json
from easysettings import EasySettings
from pathlib import Path
import shutil
import dill
import os
from joblib import dump
import zipfile
from .utils import zipdir, getApiKey, generate_requirements_file, auth, get_model, new_version, deploy_version, find_version

api_host = 'https://api.inferrd.com'

settings = EasySettings(str(Path.home()) + "/.inferrd.conf")

__all__ = [
    'indextools',
    'doctools'
]

def __main__():
  print('Hi')

# arguments
# includeFailures=True/False
def get_requests(name, **kwargs):
  model = get_model(name)
  api_key = getApiKey()

  includeFailures = False
  version = None
  limit = 100
  page = 0

  if 'limit' in kwargs:
    limit = kwargs['limit']

  if 'page' in kwargs:
    page = kwargs['page']

  if 'includeFailures' in kwargs:
    includeFailures = kwargs['includeFailures']

  if 'version' in kwargs:
    v = find_version(model['id'], kwargs['version'])
    version = v['id']

  url = api_host + '/service/' + model['id'] + '/requests?' + ('responseStatus=200&' if not includeFailures else '') + 'limit=' + str(limit) + '&page=' + str(page) + ('&version=' + version if version else '')

  print(url)

  r = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()

def deploy(model, **kwargs):
  if(getApiKey() == ''):
    print('No api key. Use inferrd.auth() first.')
    exit()

  prediction_fn = model
  name = kwargs['name']
  
  if prediction_fn is None:
    print('Empty function model. Make sure the first argument is a function.')
    exit()

  model = get_model(name)

  version = new_version(model['id'])

  print('> Preping model for deployment')

  if os.path.exists('./model.dill'):
    os.remove('./model.dill')

  dill.dump(prediction_fn, open('./model.dill', mode='wb'), recurse=True)

  if os.path.exists('./reqs.txt'):
    os.remove('./reqs.txt')

  generate_requirements_file()

  zipf = zipfile.ZipFile('model.zip', 'w', zipfile.ZIP_DEFLATED)
  zipf.write('./model.dill', './model.dill')
  zipf.write('./reqs.txt', './requirements.txt')

  if 'setup' in kwargs:
    setupFile = open('./setup.sh', 'w')
    setupFile.write(kwargs['setup'])
    setupFile.close()
    zipf.write('./setup.sh', './setup.sh')

  zipf.close()
  
  # upload to storage
  print('> Uploading model')
  f = open("./model.zip", 'rb')
  r = requests.put(version['signedUpload'], data=f, headers={'Content-Type': 'application/zip'})

  print('> Deploying version v' + str(version['number']))
  deploy_version(version['id'])

  os.remove('./model.zip')
  os.remove('./model.dill')
  os.remove('./reqs.txt')

  if 'setup' in kwargs:
    os.remove('./setup.sh')

  print('Your model is now deploying! Try it out using this code:\n')
  print('inferrd.get(\'{0}\')([1,2])'.format(name))
  return version['number']


# ------ TENSORFLOW
def deploy_tf(tf_model, name):
  if(getApiKey() == ''):
    print('No api key. Use inferrd.auth() first.')
    exit()

  print('> Saving model to folder')

  if tf_model is None:
    print('Empty tensorflow model. Make sure the first argument is a TensorFlow v2 model.')
    exit()

  model = get_model(name)

  version = new_version(model['id'])

  if os.path.exists('./inferrd-model'):
    shutil.rmtree('./inferrd-model')

  import tensorflow as tf

  tf.saved_model.save(tf_model, './inferrd-model')
    
  print('> Zipping model for upload')

  if os.path.exists('./model.zip'):
    os.remove('./model.zip')

  zipf = zipfile.ZipFile('model.zip', 'w', zipfile.ZIP_DEFLATED)
  zipdir('./inferrd-model', zipf) 
  zipf.close()

  # upload to storage
  print('> Uploading model')
  f = open("./model.zip", 'rb')
  r = requests.put(version['signedUpload'], data=f, headers={'Content-Type': 'application/zip'})

  print('> Deploying version v' + str(version['number']))
  deploy_version(version['id'])

  shutil.rmtree('./inferrd-model')
  #os.remove('./model.zip')

  print('> TensorFlow Model deployed')
  return version['number']

# ------ SCIKIT
def deploy_scikit(scikit_model, name):
  if(getApiKey() == ''):
    print('No api key. Use inferrd.auth() first.')
    exit()

  print('> Saving model to folder')

  if scikit_model is None:
    print('Empty Scikit model. Make sure the first argument is a Scikit Learn model.')
    exit()

  model = get_model(name)

  version = new_version(model['id'])

  if os.path.exists('./inferrd-scikit.joblib'):
    os.remove('./inferrd-scikit.joblib')

  dump(scikit_model, './inferrd-scikit.joblib')

  print('> Zipping model for upload')

  if os.path.exists('./model.zip'):
    os.remove('./model.zip')

  zipf = zipfile.ZipFile('model.zip', 'w', zipfile.ZIP_DEFLATED)
  zipf.write('./inferrd-scikit.joblib', './model.joblib')
  zipf.close()

  # upload to storage
  print('> Uploading model')
  f = open("./model.zip", 'rb')
  r = requests.put(version['signedUpload'], data=f, headers={'Content-Type': 'application/zip'})

  print('> Deploying version v' + str(version['number']))
  deploy_version(version['id'])

  os.remove('./inferrd-scikit.joblib')
  os.remove('./model.zip')

  print('> Scikit Model deployed')
  return version['number']

# ------ SPACY
def deploy_spacy(nlp_model, name):
  if(getApiKey() == ''):
    print('No api key. Use inferrd.auth() first.')
    exit()

  print('> Saving model to folder')

  if nlp_model is None:
    print('Empty spaCy model. Make sure the first argument is a spaCy model.')
    exit()

  model = get_model(name)

  version = new_version(model['id'])

  if os.path.exists('./inferrd-model'):
    shutil.rmtree('./inferrd-model')

  tf.saved_model.save(tf_model, './inferrd-model')
    
  print('> Zipping model for upload')

  if os.path.exists('./model.zip'):
    os.remove('./model.zip')

  zipf = zipfile.ZipFile('model.zip', 'w', zipfile.ZIP_DEFLATED)
  zipdir('./inferrd-model', zipf) 
  zipf.close()

  # upload to storage
  print('> Uploading model')
  f = open("./model.zip", 'rb')
  r = requests.put(version['signedUpload'], data=f, headers={'Content-Type': 'application/zip'})

  print('> Deploying version v' + str(version['number']))
  deploy_version(version['id'])

  shutil.rmtree('./inferrd-model')
  #os.remove('./model.zip')

  print('> Model deployed')
  return version['number']
  
def get_request_history(apiKey, kwargs):
  print('Getting request')

def call_model(serveKey, payload):
  r = requests.post(api_host + '/infer/' + serveKey + '/predict', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
  return r.json()

def get(modelName):
  model = get_model(modelName)
  serveKey = model['key']

  def infer(payload):
    r = requests.post(api_host + '/infer/' + serveKey + '/predict', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    return r.json()

  return infer