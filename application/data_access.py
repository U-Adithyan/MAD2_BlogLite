from application.database import db
from application.models import *
from flask_caching import Cache

from flask import current_app as app
cache = Cache(app)
app.app_context().push()

@cache.cached(timeout=100, key_prefix= 'get_all_users')
def get_users_all():
    users = User.query.all()
    return users

@cache.memoize(100)
def get_feed_posts(user_name):
    return db.session.query(Post,Follow_Status)\
        .filter(Follow_Status.follower == user_name,Post.username == Follow_Status.following)\
            .order_by(Post.upload_date.desc()).all()

@cache.memoize(100)
def get_my_posts(user_name):
    posts = db.session.query(Post).filter(Post.username==user_name).order_by(Post.upload_date.desc()).all()
    return posts