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
        user_img_data.append({'img_id': img.img_id,
                              'date_uploaded': img.img_dateuploaded,
                              'img_location': img.img_location,
                              'caption': img.caption})
    return jsonify(user_img_data)


@app.route('/api/newsfeed_data')
def get_newsfeed_data():
    all_follower_data = []
    json_follower_data = []
    all_follower_data = crud.get_follower_data(str(session['user_id']))
    for each_follower_data in all_follower_data:
        print(each_follower_data)
        print(each_follower_data[0])
        json_follower_data.append({'poster_firstname': each_follower_data[1],
                              'poster_lastname': each_follower_data[2],
                              'img_location': each_follower_data[4],
                              'img_dateuploaded': each_follower_data[5],
                              'img_id': each_follower_data[3],
                              'caption': each_follower_data[6]})

    return jsonify(json_follower_data)


@app.route('/profile')
def show_newsfeed():
    return render_template('profile.html', username=session['name'])


@app.route('/unfollow')
def unfollow_user():
    user = crud.remove_follower
    return render_template('/', username=session['name'])
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

    
    
