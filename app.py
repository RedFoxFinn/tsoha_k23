"""
  app.py
  
  main file of the application and triggers configuration of the application when run
  `flask run` or `invoke start`
"""
from flask import Flask

from tools.config_module import SECRET_KEY, APP_NAME

application = Flask(__name__,
                    template_folder="templates",
                    static_folder='static')
application.config["SECRET_KEY"] = SECRET_KEY

@application.context_processor
def set_global_html_variables():
    """
      set_global_html_variable

      function that adds APP_NAME to applications context globally
    """
    template_config = {'app_name': APP_NAME}
    return template_config


import routes.management    # pylint: disable=unused-import,disable=wrong-import-position
import routes.frontpage     # pylint: disable=unused-import,disable=wrong-import-position
import routes.statistics    # pylint: disable=unused-import,disable=wrong-import-position
import routes.password      # pylint: disable=unused-import,disable=wrong-import-position
import routes.register      # pylint: disable=unused-import,disable=wrong-import-position
import routes.login         # pylint: disable=unused-import,disable=wrong-import-position
import routes.init_site     # pylint: disable=unused-import,disable=wrong-import-position
