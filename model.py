from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_firstname = db.Column(db.String)
    user_lastname = db.Column(db.String)
    user_email = db.Column(db.String, unique=True)
    user_pswd = db.Column(db.String)
    user_profile_img = db.Column(db.String)
    user_location=db.Column(db.String)

    def __init__(self, user_firstname, user_lastname, user_email, user_pswd, user_profile_img, user_location):
        self.user_firstname = user_firstname
        self.user_lastname = user_lastname
        self.user_email = user_email
        self.user_pswd = user_pswd
        self.user_profile_img = user_profile_img
        self.user_location=user_location

class Follower(db.Model):
    __tablename__ = 'followers'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

class Image(db.Model):
    __tablename__ = 'images'

    img_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    img_dateuploaded = db.Column(db.DateTime)
    img_location = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    caption = db.Column(db.String)
    orientation = db.Column(db.String)

    user = db.relationship('User', backref='images')

    def __init__(self, img_dateuploaded, img_location, user_id, caption, orientation):
        self.img_dateuploaded = img_dateuploaded
        self.img_location = img_location
        self.user_id = user_id
        self.caption = caption
        self.orientation = orientation


class Comment(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment_date = db.Column(db.DateTime)
    comment_text = db.Column(db.String)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    img_id = db.Column(db.Integer, db.ForeignKey('images.img_id'))
    
    user = db.relationship('User', backref='comments')
    img = db.relationship('Image', backref='comments')



def connect_to_db(flask_app, db_uri='postgresql:///frames', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app
    connect_to_db(app)