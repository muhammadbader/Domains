from WebDomains import db
import pandas as pd


# this is for slq server
# from sqlalchemy import create_engine

# todo: get username and password, driver, database, server to connect to sqlServer
# step 1: connecting to database

# DATATASE_CONECTION = 'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
# engine = create_engine(DATATASE_CONECTION)
# connection = engine.connect()


# # step 2: fetching data from database
# data = pd.read_sql_query("some sql query", connection)
# # do some stuff on data
# # step 3: send back manipulated data to slq sever
# data.to_sql('Border_Cross_Entry_Data$', con=engine, if_exists='append', index=False, chunksize=50)


def add_user(user):
    '''
    adds new user to the database
    :param user:
    :return:
    '''
    db.session.add(user)
    db.session.commit()


# done
def change_password(name, new):
    user = search_user_by_name(name)
    try:
        user.password = new
        db.session.commit()
        res = 'successfully changed password'
    except Exception as _:
        res = 'failed ot change password'
    return res


def check_password(name, old):
    user = search_user_by_name(name)
    return old == user.password


# todo: change username
# todo: check
def update_email(name, new_email):
    user = search_user_by_name(name)
    user.email = new_email
    db.session.commit()


# todo: refactor : without user
def change_email(user, new_email):
    if user.email == new_email:
        # todo: flash a message says cannot change the email to the same old email
        pass
    exists = Users.query.filter_by(email=new_email).first()
    if exists:
        # todo: flash a message says email already exists
        pass
    else:
        update_email(user, new_email)


def delete_by_email(email):
    to_delete = Users.query.filter_by(email=email)
    for usr in to_delete:
        db.session.delete(usr)
    db.session.commit()
    return to_delete


def delete_by_name(name):
    to_delete = Users.query.filter_by(name=name)
    for usr in to_delete:
        db.session.delete(usr)
    db.session.commit()
    return to_delete


############################## Database classes ###################################################

class Users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)
    email = db.Column('email', db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # relations = db.relationship('Another table name', backref='column name', lazy=True)
    # todo: check ForeignKey
    # in the other table specify into db.Column(column type, db.ForeignKey(''))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f'username: [{self.name}], email: [{self.email}]'


def add_new_user(name, email, password):
    '''
    adds user to the database
    :param name: str
    :param email: str
    :param password: str
    :return:
        Users object represents the user
    '''
    user = Users(name, email, password)
    add_user(user)
    return user


# todo: make it private
def search_user_by_name(name):
    '''
    searches the database for the user by name
    :param name:
    :return:
        Users object
    '''
    return Users.query.filter_by(name=name).first()


def search_user_by_email(email):
    '''
    searches the database for the user by email
    :param email:
    :return:
    '''
    return Users.query.filter_by(email=email).first()


def search_user(name, email):
    '''
    checks if the username and email already exists
    :param name: str
    :param email: str
    :return: (bool)
    '''
    found = Users.query.filter_by(email=email).first()
    if found:
        return True
    found = Users.query.filter_by(name=name).first()
    return found


def all_users():
    return Users.query.all()
