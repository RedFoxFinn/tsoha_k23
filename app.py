
from flask import Flask

from modules.config_module import SECRET_KEY, APP_NAME

application = Flask(__name__, template_folder="templates",
                    static_folder='static')
application.config["SECRET_KEY"] = SECRET_KEY


@application.context_processor
def set_global_html_variables():
    template_config = {'app_name': APP_NAME}
    return template_config
