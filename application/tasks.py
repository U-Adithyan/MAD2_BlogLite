import csv
import requests
from celery.schedules import crontab
from json import dumps
from jinja2 import Template
import datetime

from application.workers import celery
from application import mail
from application.data_access import *
from application.models import *

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender,**kwargs):
     sender.add_periodic_task(crontab(minute=5,hour=20),reminder.s(), name='reminder')
     sender.add_periodic_task(crontab(0, 0, day_of_month='1'),monthly_mail.s(), name='mail')

@celery.task()
def monthly_mail():
     users = User.query.all()
     #bankers definition of a month
     limit = (datetime.datetime.now() - datetime.timedelta(days = 30)).strftime("%Y-%m-%d %H:%M:%S")
     for user in users:
          blog_num = Post.query.filter(Post.username == user.username,limit < Post.upload_date).count()
          blogs = Post.query.filter(Post.username == user.username,limit < Post.upload_date).all()
          follower_count = Follow_Status.query.filter_by(following = user.username).count()
          msg = ""
          with open("mail.html") as f:
               template = Template(f.read())
               msg = template.render(name = user.username,blog_num = blog_num,followers = follower_count,blogs = blogs)
          mail.send_mail(user.email,subject = "BlogLite2 Monthly Report", message = msg)
     return "OK",200

@celery.task()
def reminder():
     limit = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d %H:%M:%S")
     users = User.query.all()
     for user in users:
          if user.webhook != '':
               latest_time = latest_post_time(user.username)
               if limit > latest_time:
                    data = {'text':"Hi "+ user.username +", we haven't seen you in a day. Post something!!!"}
                    r = requests.post(url = user.webhook, data = dumps(data) )
     return "OK",200
          
     

@celery.task()
def get_post(user_name,id):
    path = "./static/files/"+user_name+"_post_" + str(id) + ".csv"
    headers = ['Name', 'Caption', 'Date', 'User']
    data = get_post_export(user_name,id)
    with open(path, 'w', encoding='UTF8', newline='') as f:
         writer = csv.writer(f)
         writer.writerow(headers)
         writer.writerow(data)
    return path

@celery.task()
def get_posts(user_name):
    path = "./static/files/"+user_name+".csv"
    headers = ['Name', 'Caption', 'Date']
    data = get_posts_export(user_name)
    with open(path, 'w', encoding='UTF8', newline='') as f:
         writer = csv.writer(f)
         writer.writerow(headers)
         writer.writerows(data)
    return path
