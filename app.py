
from flask import Flask

from tools.config_module import SECRET_KEY,APP_NAME

application = Flask(__name__,
                    template_folder="templates",
                    static_folder='static')
application.config["SECRET_KEY"] = SECRET_KEY


@application.context_processor
def set_global_html_variables():
    template_config = {'app_name': APP_NAME}
    return template_config

import routes.frontpage
import routes.init_site
import routes.login
import routes.register
import routes.password
import routes.statistics
import routes.management