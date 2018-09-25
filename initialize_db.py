from jarvis_run import db, jarvis_app
from jarvis.models import models

db.init_app(jarvis_app)
db.create_all(app=jarvis_app)


