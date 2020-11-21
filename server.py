from flask import Flask, render_template, redirect, flash, session, request, jsonify
import jinja2
from model import User, Comment, Follower, Image, connect_to_db
import crud


app = Flask(__name__)
connect_to_db(app)
app.secret_key = "fake-password"


@app.route('/')
def index():
    if session.get('name', None) is None:
        return redirect('/login')
    else:
        print(session['name'])
        print(session['user_id'])
        return render_template("newsfeed.html", username=session['name'])


@app.route('/login', methods=["GET"])
def show_login():
    return render_template('login.html')


@app.route('/login', methods=["POST"])
def process_login():
    email = request.form["email"]
    password = request.form["password"]

    user = crud.get_user_by_email(email)

    if user is None:
        flash("No user with this email found")
        return redirect("/login")
    else:
        if user.user_pswd == password:
            flash("Login Successful")
            session['name'] = user.user_firstname
            session['user_id'] = user.user_id
            print(session['user_id'])
            return redirect("/")
        else:
            flash("Incorrect Password, Try again")
            return redirect("/login")


@app.route('/api/profile_data')
def get_user_data():
    user_img_data = []
    print(session['user_id'])
    img_data = crud.get_user_data(str(session['user_id']))
    for img in img_data:
        comments = get_comment_info(img.img_id)
        user_img_data.append({'img_id': img.img_id,
                              'date_uploaded': img.img_dateuploaded,
                              'img_location': img.img_location,
                              'caption': img.caption,
                              'comments': comments})
    return jsonify(user_img_data)



@app.route('/api/<img_id>/comment_data')
def get_comment_info(img_id):

    comments = []
    comment_data = crud.get_comment_data(img_id)

    for comment in comment_data:
        comments.append({'img_id': comment.img_id,
                        'comment_date': comment.comment_date,
                        'commenter_id':comment.user_id,
                        'commenter_firstname':comment.user_firstname,
                        'commenter_lastname': comment.user_lastname,
                        'comment_text':comment.comment_text,
        })

    return comments



@app.route('/api/newsfeed_data')
def get_newsfeed_data():
    all_follower_data = []
    json_follower_data = []
    all_follower_data = crud.get_follower_data(str(session['user_id']))
    for each_follower_data in all_follower_data:
        print(each_follower_data)
        print(each_follower_data[0])
        json_follower_data.append({'follower_firstname': each_follower_data[1],
                              'follower_lastname': each_follower_data[2],
                              'img_location': each_follower_data[4],
                              'img_dateuploaded': each_follower_data[5],
                              'img_id': each_follower_data[3],
                              'caption': each_follower_data[6],
                              'follower_id': each_follower_data[0]})

    return jsonify(json_follower_data)


@app.route('/profile')
def show_newsfeed():
    return render_template('profile.html', username=session['name'])


@app.route('/unfollow/<follower_id>',  methods=["DELETE"])
def unfollow_user(follower_id):

    # need to convert follower_id back to a json from a string
    print(follower_id)
    user = crud.remove_follower(session['user_id'], follower_id)
    return render_template("newsfeed.html", username=session['name'])


@app.route('/upload')
def upload():
    return render_template('upload.html')  

@app.route('/img_upload', methods=["POST"])
def upload_an_image():

    img_location = request.form["url"]
    caption = request.form["caption"]
    img_dateuploaded = request.form["created_at"]

    crud.create_img(img_dateuploaded, img_location, session['user_id'], caption)

    return redirect('/profile')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

    
    
