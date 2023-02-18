
from flask import Flask

from tools import config_module as config

application = Flask(__name__,
                    template_folder="templates",
                    static_folder='static')
application.config["SECRET_KEY"] = config.SECRET_KEY


@application.context_processor
def set_global_html_variables():
    template_config = {'app_name': config.APP_NAME}
    return template_config
