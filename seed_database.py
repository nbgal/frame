import os
import json
from random import choice, randint
from datetime import datetime

import model
import server
import crud


os.system('dropdb frames')
os.system('createdb frames')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/users.json') as f:
    user_data = json.loads(f.read())

users_in_db = []
for user in user_data:
    user_firstname, user_lastname = (user['user_firstname'], user['user_lastname'])
    user_email = f'{user_firstname}_{user_lastname}@test.com'
    user_pswd = 'test'

    user = crud.create_user(user_firstname, user_lastname, user_email, user_pswd)

with open('data/images.json') as f:
    image_data = json.loads(f.read())

image_in_db = []
for image in image_data:
    img_dateuploaded, img_location, user_id, caption = (image['img_dateuploaded'], image['img_location'], image['user_id'], image['caption'])

    img = crud.create_img(img_dateuploaded, img_location, user_id, caption)

with open('data/followers.json') as f:
    followers_data = json.loads(f.read())

followers_in_db = []
for follower in followers_data:
    follower_id, user_id = (follower['follower_id'], follower['user_id'])

    follower = crud.add_follower(user_id, follower_id)


with open('data/comments.json') as f:
    comments_data = json.loads(f.read())

comments_in_db = []
for comment in comments_data:
    comment_date, commenter_id, img_id, comment_text = (comment['comment_date'], comment['commenter_id'], comment['img_id'], comment['comment_text'])

    comment = crud.add_comment(comment_date, commenter_id, img_id, comment_text)


