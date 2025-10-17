import sys
import os

# 🔹 Path to your cloned project folder
project_path = '/home/sathvikreddy/locallibrary-main-2'
if project_path not in sys.path:
    sys.path.append(project_path)

# 🔹 Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'locallibrary.settings'

# 🔹 Activate virtualenv
activate_env = os.path.join(project_path, '.venv/bin/activate_this.py')
with open(activate_env) as file_:
    exec(file_.read(), dict(__file__=activate_env))

# 🔹 Start Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
