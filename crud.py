"""CRUD operations."""

from model import db, User, Image, Follower, Comment, connect_to_db


def create_user(user_firstname, user_lastname, user_email, user_pswd):
    """Create and return a new user."""

    user = User(user_firstname=user_firstname, user_lastname=user_lastname, user_email=user_email, user_pswd=user_pswd)

    db.session.add(user)
    db.session.commit()

    return user


def create_img(img_dateuploaded, img_location, user_id, caption):
    """Create and return a new user."""

    image = Image(img_dateuploaded=img_dateuploaded, img_location=img_location, user_id=user_id, caption=caption)

    db.session.add(image)
    db.session.commit()

    return image


def add_follower(user, follower):
    exists = Follower.query.filter(Follower.user_id == user, Follower.follower_id == follower).first()
    if exists is None:
        follower = Follower(follower_id=follower, user_id=user)
        db.session.add(follower)
        db.session.commit()

    # return follower


def remove_follower(user, follower):
    exists = Follower.query.filter(Follower.user_id == user, Follower.follower_id == follower).first()
    print(exists)
    if exists is not None:
        Follower.query.filter(Follower.user_id == user, Follower.follower_id == follower).delete()
        db.session.commit()


def get_user_by_email(email):
    return User.query.filter(User.user_email == email).first()


def add_comment(comment_date, commenter_id, img_id, comment_text):

    comment = Comment(comment_date=comment_date, commenter_id=commenter_id, img_id=img_id, comment_text=comment_text)
    db.session.add(comment)
    db.session.commit()
    return comment


def get_user_data(user_id):

    # data = db.session.query(User.user_firstname, User.user_lastname, Image.img_id, Image.img_id, Image.img_location, Image.img_dateuploaded, Image.caption, Comment.comment_date, Comment.comment_text, Comment.comment_id).join(Image, Image.user_id == User.user_id).filter(Image.user_id == user_id).join(Comment, Comment.img_id == Image.img_id).order_by(Image.img_dateuploaded.desc()).all()

    # return data


   return Image.query.filter(Image.user_id == user_id).order_by(Image.img_dateuploaded.desc()).all()


def get_follower_data(user_id):
    
    data = db.session.query(User.user_id, User.user_firstname, User.user_lastname, Image.img_id, Image.img_location, Image.img_dateuploaded, Image.caption).join(Follower, Follower.follower_id == User.user_id).filter(Follower.user_id == user_id).join(Image).all()
    
    return sorted(data, key=lambda x: x[5], reverse=True)

def get_comment_data(img_id):

    comments = db.session.query(Comment.comment_date, Comment.comment_text, Comment.comment_id, Image.img_id, User.user_id, User.user_firstname, User.user_lastname).join(Image, Image.img_id == Comment.img_id).filter(Comment.img_id == img_id).join(User, User.user_id == Comment.commenter_id).order_by(Comment.comment_date.desc()).all()
    

    return comments


if __name__ == '__main__':
    from server import app
    connect_to_db(app)