from application.database import db
from application.models import *
from flask_caching import Cache
from flask import current_app as app

cache = Cache(app)
app.app_context().push()

@cache.cached(timeout=10, key_prefix= 'get_all_users')
def get_users_all():
    users = User.query.all()
    return users

@cache.memoize(10)
def get_feed_posts(user_name):
    return db.session.query(Post,Follow_Status)\
        .filter(Follow_Status.follower == user_name,Post.username == Follow_Status.following)\
            .order_by(Post.upload_date.desc()).all()

@cache.memoize(1)
def get_my_posts(user_name):
    posts = db.session.query(Post).filter(Post.username==user_name).order_by(Post.upload_date.desc()).all()
    return posts

@cache.memoize(10)
def get_post_export(name,id):
    post = Post.query.filter_by(username=name,post_id=id).first()
    return [post.name,post.caption,post.upload_date,post.username]

@cache.memoize(10)
def get_posts_export(name):
    posts = Post.query.filter_by(username=name).all()
    ans=[]
    for post in posts:
        ans.append([post.name,post.caption,post.upload_date])
    return ans

@cache.memoize(10)
def latest_post_time(name):
    post = db.session.query(Post).filter(Post.username==name).order_by(Post.upload_date.desc()).first()
    if post is None:
        return str(0)
    return post.upload_date