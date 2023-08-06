import zipfile
import os
from easysettings import EasySettings
from pathlib import Path
import requests

try:
    from importlib import metadata
except ImportError: # for Python<3.8
    import importlib_metadata as metadata

api_host = 'https://api.inferrd.com'

IN_COLAB = False
try:
  import google.colab
  IN_COLAB = True
except:
  IN_COLAB = False

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            filePath = os.path.join(root, file)
            inZipPath = os.path.relpath(os.path.join(root, file), os.path.join(path, '..'))
            # remove base folder
            ziph.write(filePath, inZipPath.replace(path.split('/')[-1] + '/', ''))


def auth(key):
  settings = getEasySettings()
  settings.set('api_key', key)
  settings.save()

def getEasySettings():
  # google collab returns /root for Path.home() and it breaks
  settings = EasySettings(str(Path() if IN_COLAB else Path.home()) + "/.inferrd.conf")
  return settings

def getApiKey():
  settings = getEasySettings()
  return settings.get('api_key')

def get_model(name):
  api_key = getApiKey()

  r = requests.get(api_host + '/service/find/' + name, headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()

def new_version(modelId):
  api_key = getApiKey()

  r = requests.post(api_host + '/service/' + modelId + '/versions', headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()

def deploy_version(versionId, **kwargs):
  api_key = getApiKey()

  obj = {
    "sampleInputs": kwargs['sampleInputs'] if 'sampleInputs' in kwargs else None
  }

  r = requests.post(api_host + '/version/' + versionId + '/deploy', headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key}, json=obj)

  return r.json()

def find_version(modelId, name):
  api_key = getApiKey()

  r = requests.get(api_host + '/service/' + modelId + '/versions/find/' + name, headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()

def generate_requirements_file():
  dists = metadata.distributions()

  with open('./reqs.txt', 'a') as requirementsFile:
    for dist in dists:
      name = dist.metadata["Name"]
      version = dist.version

      # don't install version 0.0.0
      if str(version) == "0.0.0":
        continue

      # don't install colab packages
      if "colab" in name:
        continue

      requirementsFile.write(f'{name}=={version}\n')