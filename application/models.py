from application.database import db
from flask_security import UserMixin,RoleMixin

roles_users = db.Table('roles_users',
                      db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                      db.Column('role_id',db.Integer,db.ForeignKey('role.id')))

class User(db.Model,UserMixin):
  __tablename__='user'
  id = db.Column(db.Integer,autoincrement=True,primary_key=True)
  email = db.Column(db.String(255))
  username = db.Column(db.String(255), unique=True)
  password = db.Column(db.String(255))
  fs_uniquifier = db.Column(db.String(255),unique=True,nullable=False)
  active = db.Column(db.Boolean())
  dp_location = db.Column(db.String(255))
  roles = db.relationship('Role',secondary=roles_users,backref=db.backref('user',lazy='dynamic'))
  posts = db.relationship('Post',backref=db.backref('user'),lazy="subquery")
  latest_post_id = db.Column(db.Integer,default=0)

class Role(db.Model,RoleMixin):
  __tablename__='role'
  id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
  name = db.Column(db.String(80),unique=True)
  description = db.Column(db.Text)

class Post(db.Model):
  __tablename__ = 'post'
  id = db.Column(db.Integer,autoincrement=True,primary_key=True)
  post_id = db.Column(db.Integer)
  username = db.Column(db.String(255), db.ForeignKey("user.username"))
  name = db.Column(db.String(255))
  caption = db.Column(db.Text())
  image = db.Column(db.String(255))
  upload_date = db.Column(db.String(255))

class Follow_Status(db.Model):
  __tablename__ = 'follow_status'
  id = db.Column(db.Integer,autoincrement=True,primary_key=True)
  follower = db.Column(db.String(255), db.ForeignKey("user.username"))
  following = db.Column(db.String(255), db.ForeignKey("user.username"))