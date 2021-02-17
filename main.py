from flask import Flask, redirect, url_for, render_template, request, session, flash
import search
# session is a dictionary and like cookies
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'muha'  # make it something complicated
# timeout for remembering the session data, by default
app.permanent_session_lifetime = timedelta(hours=6)


@app.route('/index')
def index():
    return render_template("index.html")


# a decorator for deciding where to go when running
@app.route("/")
def home():
    # return "hello this is the main page <h1>HEllo!!!</h1>"
    # return render_template("index.html")
    return redirect((url_for("welcome_page")))


@app.route("/login", methods=['POST', 'GET'])
def login():
    if session['logged_in']:
        flash('already logged in, signout to log in to a new account')
        return redirect((url_for('search')))
    if request.method == 'POST':
        ''' this makes this session permanent'''
        session.permanent = True
        usr = request.form['nm']
        session['user'] = usr
        email = '@' in usr
        passw = request.form['pass']
        if not passw:
            # todo: print in red font, missing password and timeout
            pass
        session['psw'] = passw
        check_pass = ''
        if email:
            # todo:get password from db by email
            pass
        else:
            # todo: get password from db by username
            pass
        session['logged_in'] = True
        return redirect((url_for("search")))
    return render_template("login.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    # return render_template("login.html")
    if request.method == 'POST':
        passw = request.form['pass']
        conf = request.form['confirm']
        if passw == conf:
            usr_nm = request.form['nm']
            email = request.form['mail']
            session['user'] = usr_nm
            session['pwd'] = 'passw'
            # todo: check if the username and email exists
            # todo: here we will update the db
            # todo: redirect at the search page
            return redirect((url_for("search")))
        else:
            # wrong password
            # todo: send a message says that wrong password
            return redirect((url_for("signup")))
    else:
        return render_template("signup.html")


@app.route("/welcome")
def welcome_page():
    # todo: check if the user is logged in or not first
    if 'user' in session:
        return redirect(url_for('search'))
    else:
        return redirect(url_for('login'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    if session['logged_in']:
        flash('ready for some domain search')
        if request.method == 'POST':
            if request.form.get('search_button') == 'signout':
                return delete_and_login_page()
            dom = request.form['dom']
            if dom:
                # todo: start searching for
                pass
            return redirect(url_for('search_results'))
        else:
            return render_template('search.html', user=session['user'])
    else:
        return redirect(url_for('login'))


def delete_and_login_page():
    if 'user' in session:
        flash(f'You Have been logged out, {session["user"]}', 'info')  # for flash we need to update the html file
    for key in ['user', 'psw']:
        if key in session:
            session.pop(key, None)

    session['logged_in'] = False
    return redirect(url_for('login'))


@app.route('/Search Results', methods=['POST', 'GET'])
def search_results():
    if request.method == 'POST':
        if request.form['search_result_button'] == 'signout':
            return delete_and_login_page()
    return render_template('search_results.html')


# dump test
@app.route('/<usr>')
def user(usr):
    return f'<p>{usr}</p>'


# dump test
@app.route('/dummy')
def admin():
    # redirect to the function name
    # return redirect((url_for("home")))
    return redirect((url_for("user", usr='Admin')))


if __name__ == '__main__':
    app.run(debug=True)

'''
how to modify an html file with python
using React and JS

'''
