import os
from flask import Flask
from application import config
from application.config import DevelopConfig
from application.database import db
from application.models import User,Role
from flask_security import Security, SQLAlchemySessionUserDatastore


app=None

def create_app():
  app=Flask(__name__,template_folder="templates")

  print("Starting Development")
  app.config.from_object(DevelopConfig)

  db.init_app(app)
  app.app_context().push()

  user_datastore =  SQLAlchemySessionUserDatastore(db.session,User,Role)
  security = Security(app,user_datastore)
  
  return app

app = create_app()

from application.controllers import *
from application.api import *

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)