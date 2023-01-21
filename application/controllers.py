from flask import Flask,request,flash
from flask import render_template,redirect,jsonify
from flask import current_app as app
from datetime import datetime
from application.database import db
from application.models import *

@app.route('/')
def start():
  return redirect('/login')

@app.route('/<string:username>/dashboard')
def dashboard(username):
  return render_template("dashboard.html")

@app.route('/<string:username>/profile')
def profile(username):
  return render_template("profile.html")

@app.route('/<string:username>/search')
def search(username):
  return render_template(
    "search.html",
    username=username
  )

@app.route('/<string:username>/followers')
def followers_page(username):
  return render_template("followers.html")

@app.route('/<string:username>/following')
def following_page(username):
  return render_template("following.html")

@app.route('/<string:username>/view/profile')
def view_profile(username):
  return render_template("view_profile.html")

@app.route('/<string:username>/make_blog')
def make_blog(username):
  return render_template("make_post.html")

@app.route('/<string:username>/post/<int:post_id>/update_post')
def update_post(username,post_id):
  return render_template("update_post.html")

##Failure redirects

@app.route('/login_failed/<int:code>')
def login_failure(code):
  print(code)
  if(code == 401):
    flash("Login failed: Invalid Password")
  elif(code == 404):
    flash("Login failed: Non-Existent User")
  else:
    flash("Login failed: Invalid Input - Enter Valid Values")
  
  return redirect('/')

@app.route('/register_failed/<int:code>')
def register_failure(code):
  if(code==400):
    flash("Register failed: Existing username")
  else:
    flash("Register failed: Invalid Input")
  return redirect('/register')

@app.route('/<string:username>/register_failed/<int:code>')
def register_image_failure(username,code):
  current = User.query.filter_by(username=username).first()
  db.session.delete(current)
  db.session.commit()
  flash("Register failed: Please Enter a Valid Image")
  return redirect('/register')

@app.route('/access_failure')
def access_failure():
  flash("Login to Continue")
  return redirect('/')

@app.route('/<string:username>/<int:code>/post_failure')
def post_failure(username,code):
  flash("Failed to Post")
  if code!=0:
    flash("Invalid Image")
    current = User.query.filter_by(username=username).first()
    post = Post.query.filter_by(username=username,post_id=(current.latest_post_id-1)).first()
    db.session.delete(post)
    db.session.commit()
  return redirect('/'+username+'/dashboard')