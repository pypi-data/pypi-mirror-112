import sys, os
from easysettings import EasySettings
from pathlib import Path
from .serve import serve_local_model
from .deploy import deploy_current_folder

settings = EasySettings(str(Path.home()) + "/.inferrd.conf")

def main():
  command = sys.argv[1]

  if(command != 'auth' and command != 'serve' and command != 'init' and command != 'deploy'):
    print('The only command available are "auth", "serve", "init" and "deploy"')
    exit()

  if(len(sys.argv) == 2 and command == 'auth'):
    print('Missing api key. Usage: inferrd auth <api-key>')
    exit()

  if(len(sys.argv) == 2 and command == 'deploy'):
    print('Missing model name. Usage: inferrd deploy <model name or id>')
    exit()

  if(command == 'serve'):
    serve_local_model()

  if(command == 'deploy'):
    deploy_current_folder(sys.argv[2])

  if(command == 'init'):
    os.system('git clone https://github.com/inferrd/custom-environment-example')

  if(command == 'auth'):
    api_key = sys.argv[2]
    settings.set('api_key', api_key)
    settings.save()
    print('API Key has been set.')

if __name__ == '__main__':
  main()