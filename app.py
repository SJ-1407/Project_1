import os
from flask import Flask
import application.config
from application.config import LocalDevelopmentConfig
from application.database import db
from sqlalchemy.orm import scoped_session, sessionmaker
from application.models import *



app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
      app.logger.info("Currently no production config is setup.")
      raise Exception("Currently no production config is setup.")
    else:
      app.logger.info("Staring Local Development.")
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    app.logger.info("App setup complete")
   
    return app

app = create_app()








from application.controllers import *




if __name__ == '__main__':
  db.create_all()
  app.run(debug=True)


