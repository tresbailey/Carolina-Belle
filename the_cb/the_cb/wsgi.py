"""
WSGI config for the_cb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

# Activate your virtual env
activate_env=os.path.expanduser("/application/venv/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
from mezzanine.utils.conf import real_project_name

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "%s.settings" % real_project_name("the_cb"))

application = get_wsgi_application()
