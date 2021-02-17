from flask import redirect, url_for, render_template, request, session, flash
from WebDomains.database import add_new_user, search_user, all_users, update_email, delete_by_email
from WebDomains import app


# session is a dictionary and like cookies
curr_account = None

@app.route('/index')
def index():
    return render_template("index.html")


# a decorator for deciding where to go when running
@app.route("/")
@app.route("/home")
def home():
    # return "hello this is the main page <h1>HEllo!!!</h1>"
    # return render_template("index.html")
    return redirect((url_for("welcome_page")))


@app.route("/login", methods=['POST', 'GET'])
def login():
    if session.get('logged_in'):
        flash('already logged in, signout to log in to a new account')
        return redirect((url_for('search')))
    if request.method == 'POST':
        ''' this makes this session permanent'''
        session.permanent = True
        session['user'] = request.form['nm']
        email = '@' in session['user']
        passw = request.form['pass']
        if not passw:
            # todo: print in red font, missing password and timeout
            pass
        session['psw'] = passw
        check_pass = ''
        if email:
            # todo: get password from db by email
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

            # check if the username and email exists
            if not search_user(usr_nm, email):
                # here we will update the db with new account
                usr = add_new_user(usr_nm, email, passw)
                global curr_account
                curr_account = usr
                session['logged_in'] = True
                return redirect(url_for('search'))
            else:
                # todo: send a message indicates that the username or email already exists
                pass

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
        # flash('ready for some domain search')
        if request.method == 'POST':
            if request.form.get('search_button') == 'signout':
                return delete_and_login_page()
                # start searching
            dom = request.form['dom']
            if request.form.get('search_button') == 'update email':
                update_email(curr_account, dom)
            elif request.form.get('search_button') == 'delete email':
                delete_by_email(dom)

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
        flash(f'You have been logged out, {session["user"]}', 'info')  # for flash we need to update the html file
    for key in ['user', 'psw']:
        if key in session:
            session.pop(key, None)
    global curr_account
    curr_account = None

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


@app.route('/view')
def view():
    return render_template('view.html', values=all_users())
