import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config():
  DEBUG = False
  SQLITE_DB_DIR = None
  SQLALCHEMY_DATABASE_URI = None
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  WTF_CSRF_ENABLED = False
  SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
  CELERY_BROKER_URL = "redis://localhost:6379/1"
  CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
  REDIS_URL = "redis://localhost:6379"
  CACHE_TYPE = "RedisCache"
  CACHE_REDIS_HOST = "localhost"
  CACHE_REDIS_PORT = 6379
  
class DevelopConfig(Config):
  SQLITE_DB_DIR = os.path.join(basedir,"../db_directory/")
  SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(SQLITE_DB_DIR,"appdb.sqlite3")
  UPLOAD_FOLDER = os.path.join(basedir,"../static/Images/")
  DEBUG=True
  SECRET_KEY = "super secret key"
  SECURITY_PASSWORD_HASH="bcrypt"
  SECURITY_PASSWORD_SALT = "really super secret info"
  SECURITY_REGISTERABLE = True
  SECURITY_CONFIRMABLE = False
  SECURITY_SEND_REGISTER_EMAIL = False
  SECURITY_USERNAME_ENABLE =True
  SECURITY_UNAUTHORISED_VIEW = None
  WTF_CSRF_ENABLED = False
  CELERY_BROKER_URL = "redis://localhost:6379/1"
  CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
  REDIS_URL = "redis://localhost:6379"
  CACHE_TYPE = "RedisCache"
  CACHE_REDIS_HOST = "localhost"
  CACHE_REDIS_PORT = 6379
