from flask import Flask, render_template, redirect, flash, session, request, jsonify
import jinja2
from model import User, Comment, Follower, Image, connect_to_db
import crud
from datetime import datetime


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
        print(session['email'])
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
            session['email'] = user.user_email
            return redirect("/")
        else:
            flash("Incorrect Password, Try again")
            return redirect("/login")


@app.route('/account', methods=["GET"])
def show_account_create():
    return render_template('account.html')


@app.route('/search', methods=["POST"])
def get_result():

    user_email = request.form["email"]

    session['search'] = user_email
    json_page()
    print("here")
    return redirect('/search')


@app.route('/search')
def display_result():
    return render_template('search.html')


@app.route('/api/search')
def json_page():

    follower = crud.get_user_by_email(str(session['search']))
    user = crud.get_user_by_email(str(session['email']))
    print(follower, user)

    data = crud.get_user_profile_data(follower.user_id)
    exists = crud.check_follower(user.user_id, follower.user_id)
    print(data, exists)

    if exists > 0:
        followed = True
    else:
        followed = False
    return jsonify({'user_id':data[0].user_id, 'user_firstname': data[0].user_firstname, 'user_lastname':data[0].user_lastname, 'user_profile_img': data[0].user_profile_img, 'user_location': data[0].user_location, 'followed': followed})


@app.route('/account', methods=["POST"])
def account_create():

    user_firstname = request.form['user_firstname']
    user_lastname = request.form['user_lastname']
    user_email = request.form["email"]
    user_pswd = request.form['password']
    user_profile_img = request.form['user_profile_img']
    user_location = request.form['user_location']

    crud.create_user(user_firstname, user_lastname, user_email, user_pswd, user_profile_img, user_location)

    user = crud.get_user_by_email(user_email)

    session['name'] = user.user_firstname
    session['user_id'] = user.user_id
    print(session['user_id'])
    return redirect("/")


@app.route('/api/user_profile_data')
def get_user_profile_data():
    user_profile_data =[]
    data = crud.get_user_profile_data(str(session['user_id']))
    return jsonify({'user_id':data[0].user_id, 'user_firstname': data[0].user_firstname, 'user_lastname':data[0].user_lastname, 'user_profile_img': data[0].user_profile_img, 'user_location': data[0].user_location})


@app.route('/api/profile_data')
def get_user_data():
    user_img_data = []
    print(session['user_id'])
    img_data = crud.get_user_data(str(session['user_id']))
    for img in img_data:
        comments = get_comment_info(img.img_id)
        # for comment in comments:
        #     user_profile_data = crud.get_user_profile_data(comment['commenter_id'])
        #     print(user_profile_data, "\n\n")

        user_img_data.append({'img_id': img.img_id,
                               'img_orientation': img.orientation,
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
                        'commenter_profile_img': comment.user_profile_img
        })

    return comments


@app.route('/addcomment', methods=["POST"])
def add_comment():

    data = request.get_json()
    img_id = data['img_id']
    comment_text = data['Comment']
    commenter_id = session['user_id']
    comment_date = datetime.now()
    print(img_id, comment_text)
    
    crud.add_comment(comment_date, commenter_id, img_id, comment_text)
    return redirect('/')


@app.route('/api/newsfeed_data')
def get_newsfeed_data():
    all_follower_data = []
    json_follower_data = []
    all_follower_data = crud.get_follower_data(str(session['user_id']))
    for each_follower_data in all_follower_data:
        print(each_follower_data)
        print(each_follower_data[0])
        comment_data = get_comment_info(each_follower_data[3])
        json_follower_data.append({'follower_firstname': each_follower_data[1],
                              'follower_lastname': each_follower_data[2],
                              'img_location': each_follower_data[4],
                              'img_dateuploaded': each_follower_data[5],
                              'img_id': each_follower_data[3],
                              'caption': each_follower_data[6],
                              'follower_id': each_follower_data[0],
                              'comment_data': comment_data,
                              'follower_profile_img': each_follower_data[7]
                              })

    return jsonify(json_follower_data)


@app.route('/profile')
def show_newsfeed():
    return render_template('profile.html', username=session['name'])


@app.route('/unfollow/<follower_id>',  methods=["DELETE"])
def unfollow_user(follower_id):

    # need to convert follower_id back to a json from a string
    print(follower_id)
    user = crud.remove_follower(session['user_id'], follower_id)
    return redirect("/", username=session['name'])



@app.route('/follow/<follower_id>',  methods=["POST"])
def follow_user(follower_id):

    # need to convert follower_id back to a json from a string
    print(follower_id)
    user = crud.add_follower(session['user_id'], follower_id)
    return redirect("/")


@app.route('/upload')
def upload():
    return render_template('upload.html')
 

@app.route('/img_upload', methods=["POST"])
def upload_an_image():

    img_location = request.form["url"]
    caption = request.form["caption"]
    height = int(request.form["height"])
    width = int(request.form["width"])
    img_dateuploaded = request.form["created_at"]

    if height < width:
        orientation = "landscape"
    else:
        orientation = "portrait"

    print(height, width, orientation)
    crud.create_img(img_dateuploaded, img_location, session['user_id'], caption, orientation)

    return redirect('/profile')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

    
    
