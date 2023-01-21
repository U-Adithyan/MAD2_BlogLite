import os
from flask import Flask,request,jsonify,flash
from flask import render_template,redirect
from werkzeug.utils import secure_filename
from flask_security import auth_token_required
from flask import current_app as app
from datetime import datetime
from application.database import *
from application.models import *
from application.data_access import *

from time import perf_counter_ns

basedir=os.path.abspath(os.path.dirname(__file__))

@app.route('/authenticate')
@auth_token_required
def authentication():
  return jsonify({"response":"success"}),200

@app.route('/<string:username>/post/<int:post_id>/update',methods=['POST'])
@auth_token_required
def updatePost(username,post_id):
  post = Post.query.filter_by(username=username,post_id=post_id).first()
  post.name = request.form['title']
  post.caption = request.form['caption']
  post.upload_date = datetime.now()

  file = request.files.get("file")
  if file is not None:
    path = '../' + post.image
    path = os.path.join(basedir,path)
    if os.path.exists(path):
      os.remove(path)

    path = os.path.join(app.config['UPLOAD_FOLDER'], username)
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = secure_filename('post' + str(post_id) + '.' + ext)
    file.save(os.path.join(path, filename))

    location = "/static/Images/"+username+"/"+filename
    post.image = location
  db.session.commit()
  return jsonify({"response":"post_updated"}),200
    

  

@app.route('/<string:username>/post/<int:post_id>')
@auth_token_required
def get_post(username,post_id):
  post = Post.query.filter_by(username=username,post_id=post_id).first()
  if post is None:
    flash("Post does not exist.")
    return jsonify({"response":"post not found"}),404
  return jsonify({"response" : "success",
                  "title" : post.name,
                 "caption" : post.caption }),200

@app.route('/<string:username>/post/<int:post_id>/delete_post',methods=['DELETE'])
@auth_token_required
def delete_post(username,post_id):
  post = Post.query.filter_by(username=username,post_id=post_id).first()
  
  if post is None:
    return jsonify({"response":"Invalid Post"}),404

  path = '../' + post.image
  path = os.path.join(basedir,path)
  
  if os.path.exists(path):
    os.remove(path)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"response":"Post Deleted"}),200
  else:
    return jsonify({"response":"Image Missing"}),404

@app.route('/<string:username>/get_feed')
@auth_token_required
def get_feed(username):
  post_list=[]
  start = perf_counter_ns()
  feed = get_feed_posts(username)
  stop = perf_counter_ns()
  print(stop-start)
  for p, u in feed:
    post_list.append({
      "id" : p.post_id,
      "username": p.username,
      "title" : p.name,
      "caption" : p.caption,
      "image" : p.image
     })
  print(post_list)
  return jsonify({"response":"success","post_list":post_list}),200

@app.route('/<string:username>/post/<int:post_id>/posting_image',methods=["POST"])
@auth_token_required
def new_blog_image(username,post_id):

  path = os.path.join(app.config['UPLOAD_FOLDER'], username)
  file = request.files["file"]
  ext = file.filename.rsplit('.', 1)[1].lower()
  filename = secure_filename('post' + str(post_id) + '.' + ext)
  file.save(os.path.join(path, filename))

  location = "/static/Images/"+username+"/"+filename
  post = Post.query.filter_by(username=username,post_id=post_id).first()
  post.image = location
  db.session.commit()
  flash("Blog Posted")
  return jsonify({"response":"image posted","id":post_id}),200
  

@app.route('/<string:username>/posting',methods=["POST"])
@auth_token_required
def new_blog(username):
  data = request.json
  current_user = User.query.filter_by(username=username).first()
  post_id = current_user.latest_post_id
  current_user.latest_post_id += 1
  date = datetime.now()
  new_post = Post(post_id=post_id,username=username,name=data['title'],caption=data['caption'],upload_date=date)
  db.session.add(new_post)
  db.session.commit()
  return jsonify({"response":"posted","id":post_id}),200
  

@app.route('/<string:username>/get_profile')
@auth_token_required
def get_profile(username):
  current_user = User.query.filter_by(username=username).first()
  image_location = current_user.dp_location
  blog_count = Post.query.filter_by(username=username).count()
  follower_count = Follow_Status.query.filter_by(following = username).count()
  following_count = Follow_Status.query.filter_by(follower = username).count()

  post_list = []
  
  start = perf_counter_ns()
  my_posts = get_my_posts(username)
  stop = perf_counter_ns()
  print(stop-start)
  
  for p in my_posts:
    post_list.append({
      "id" : p.post_id,
      "usernamget_all_users()": p.username,
      "title" : p.name,
      "caption" : p.caption,
      "image" : p.image
     })

  
  return jsonify({"response" : "profile success", 
                  "image_location" : image_location,
                  "blog_count" : blog_count,
                  "follower_count" : follower_count,
                  "following_count" : following_count,
                  "post_list" : post_list
                 }),200

@app.route('/<string:username>/check/follow/<string:user2>')
@auth_token_required
def check_status(username,user2):
  status = Follow_Status.query.filter_by(follower = username, following = user2).first()
  if status is None:
    return jsonify({"response":"success", "status" : False}),200
  else:
    return jsonify({"response":"success", "status" : True}),200

@app.route('/<string:user1>/follows/<string:user2>',methods=["POST"])
@auth_token_required
def following(user1,user2):
  follow = Follow_Status(follower = user1, following = user2)
  db.session.add(follow)
  db.session.commit()
  return jsonify({"response":"followed"}),200

@app.route('/<string:user1>/unfollows/<string:user2>',methods=["DELETE"])
@auth_token_required
def unfollowing(user1,user2):
  unfollow = Follow_Status.query.filter_by(follower = user1, following = user2).all()
  for item in unfollow:
    db.session.delete(item)
  db.session.commit()
  return jsonify({"response":"unfollowed"}),200

@app.route('/user/<string:username>/add_dp',methods=["POST"])
@auth_token_required
def add_DP(username):
  directory = username
  path = os.path.join(app.config['UPLOAD_FOLDER'], directory)
  os.mkdir(path)
  
  file = request.files["file"]
  ext = file.filename.rsplit('.', 1)[1].lower()
  filename = secure_filename('profile.' + ext)
  file.save(os.path.join(path, filename))

  location = "/static/Images/"+directory+"/"+filename
  current_user = User.query.filter_by(username=username).first()
  current_user.dp_location = location
  db.session.commit()
  
  
  return jsonify({"response":"success"}),200

def is_followed(user1,user2):
  check = Follow_Status.query.filter_by(follower = user1, following = user2).first()
  if check is None:
    return False
  return True

@app.route('/<string:username>/get_user_list')
@auth_token_required
def get_all_users(username):
  start = perf_counter_ns()
  list = get_users_all()
  stop = perf_counter_ns()
  print(stop-start)
  ans_list = []
  for user in list:
    if user.username != username:
      ans_list.append({'username':user.username,'followed':is_followed(username,user.username)})
  return jsonify({"response":"success", "user_list" : ans_list}),200

@app.route('/<string:username>/get_following')
@auth_token_required
def get_followed_users(username):
  list = Follow_Status.query.filter_by(follower=username).all()
  ans_list = []
  for user in list:
    ans_list.append({'username':user.following,'followed':is_followed(username,user.following)})
  return jsonify({"response":"success", "user_list" : ans_list}),200

@app.route('/<string:username>/get_followers')
@auth_token_required
def get_followers(username):
  list = Follow_Status.query.filter_by(following=username).all()
  ans_list = []
  for user in list:
    ans_list.append({'username':user.follower,'followed':is_followed(username,user.follower)})
  return jsonify({"response":"success", "user_list" : ans_list}),200
