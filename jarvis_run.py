from jarvis import init_config, init_logging, init_db, jarvis_app
from slackclient import SlackClient

#  Init Configuration
app_config = init_config()

#  Init DB
logger = init_logging()

#  Setting up DB Stuff
logger.info("Setting up DB Connection")

db = init_db(jarvis_app, app_config)

#  Set up slack client connection
sc = SlackClient(app_config['slack']['bot_oauth_key'])

#  Get the routes
logger.info("Setting up routes in flask")
import jarvis.routes.heartbeat
import jarvis.routes.echo
import jarvis.routes.adduser
import jarvis.routes.page_cs
import jarvis.routes.call_router


if __name__ == '__main__':

    jarvis_app.run(host=app_config['flask']['bind_ip'],
                   port=app_config['flask']['port'],
                   debug=app_config['flask']['debug'])

