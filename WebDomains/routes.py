from flask import redirect, url_for, render_template, request, session, flash
import WebDomains.database as db
from WebDomains import app
import re

# session is a dictionary and like cookies

email_pattern = r'[\w\W]*@[\W\w\d]*\.[\d\w\W]*'


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

        login_method = request.form['nm']
        email = re.search(email_pattern, login_method)
        passw = request.form['pass']

        if not passw:
            flash('MISSING PASSWORD (RED)')
            # todo: print in red font, missing password and timeout
            return render_template("login.html")

        if email:
            account = db.search_user_by_email(email.group(0))
        else:
            account = db.search_user_by_name(login_method)

        if account:  # the account really exists
            if request.form['pass'] == account.password:  # account is ok and pass is ok
                # session['psw'] = curr_account.password
                session['name'] = account.name
                session['email'] = account.email
                session['logged_in'] = True
                return redirect((url_for("search")))
            else:
                flash('Wrong password!')
                return render_template("login.html")

        else:  # email does not exists in database
            flash('wrong name')
            return render_template("login.html")

    return render_template("login.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if session.get('logged_in'):
        flash('already logged in, signout to log in to a new account')
        return redirect((url_for('search')))
    # return render_template("login.html")
    if request.method == 'POST':
        passw = request.form['pass']
        conf = request.form['confirm']
        usr_nm = request.form['nm']
        email = request.form['mail']
        if passw == '' or email == '' or usr_nm == '':
            flash('missing some templates')
            return render_template('signup.html')
        if passw == conf:

            # check if the username and email exists
            if not db.search_user(usr_nm, email):
                # here we will update the db with new account
                usr = db.add_new_user(usr_nm, email, passw)

                session['name'] = usr_nm
                session['email'] = email
                session['logged_in'] = True

                # redirect at the search page
                return redirect(url_for('search'))
            else:
                # send a message indicates that the username or email already exists
                flash('Username of Email already exists')
                flash('try another username or email or log in')
                return render_template("signup.html")

        else:
            # wrong password
            # send a message says that wrong password
            flash('password does not match')
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
    if 'logged_in' in session and session['logged_in']:
        # flash('ready for some domain search')
        if request.method == 'POST':
            if request.form.get('search_button') == 'signout':
                return delete_and_login_page()
                # start searching
            dom = request.form['dom']
            if request.form.get('search_button') == 'update email':

                db.update_email(session['name'], dom)
            elif request.form.get('search_button') == 'delete email':
                db.delete_by_email(dom)
            elif request.form.get('search_button') == 'delete account':
                return delete_account()
            elif request.form.get('search_button') == 'change password':
                return redirect(url_for('change_pass'))

            if dom:
                # todo: start searching for
                pass
            return redirect(url_for('search_results'))
        else:
            return render_template('search.html', user=session['name'])
    else:
        return redirect(url_for('login'))


# basically works
@app.route(f'/change_password', methods=['GET', 'POST'])
def change_pass():
    if request.method == 'GET':
        return render_template('change_pass.html')
    elif request.method == 'POST':
        if request.form.get('change password') == 'back':
            return redirect(url_for('search'))
        elif request.form.get('change password') == 'confirm change':
            old = request.form['old']
            new = request.form['new']
            conf_new = request.form['confirm']

            if not db.check_password(session['name'], old):
                flash(f'wrong password {db.check_password(session["name"], old)}')
                return render_template('change_pass.html')
            if new == '':
                flash('new password cannot be empty!')
                return render_template('change_pass.html')
            if new != conf_new:
                flash('new password does not match ')
                return render_template('change_pass.html')
            if old == new:
                flash("new password should be different from old one")
                return render_template('change_pass.html')

            res = db.change_password(session['name'], new)
            flash(f'{res}')
            # todo: make something that pops a message and an option of returning to search page
            return redirect(url_for('search'))
        else:
            return redirect(url_for('search'))


# todo: delete afterwards
@app.route('/logout')
def delete_and_login_page():
    if 'name' in session:
        flash(f'You have been logged out, {session["name"]}', 'info')  # for flash we need to update the html file
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
        elif request.form['search_result_button'] == 'proceed':
            x = db.delete_by_email(session['email'])
            return redirect(url_for('user', usr=x))
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
    return redirect((url_for("user", usr=f'{session["name"]}')))


@app.route('/view')
def view():
    '''
    views all users in database
    :return:
    '''
    return render_template('view.html', values=db.all_users())


def delete_account():
    '''
    deletes account from database
    :return:
    '''
    to_delete = db.delete_by_email(session['email'])
    for de in to_delete:
        flash(f'{de}')
    session['logged_in'] = False
    return redirect(url_for('login'))


# todo: delete when finish
@app.route('/dont_call_this')
def delete_all_accounts():
    all_users = db.all_users()
    for user in all_users:
        flash(f"{user}")
        db.delete_by_email(user.email)
    session['logged_in'] = False
    return redirect(url_for('login'))
