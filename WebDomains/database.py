from WebDomains import db
import pandas as pd
# from sqlalchemy import create_engine

# DATATASE_CONECTION = 'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
# engine = create_engine(DATATASE_CONECTION)
# connection = engine.connect()


# # step 2: fetching data from database
# data = pd.read_sql_query("some sql query", connection)
# # do some stuff on data
# # step 3: send back manipulated data to slq sever
# data.to_sql('Border_Cross_Entry_Data$', con=engine, if_exists='append', index=False, chunksize=50)



def add_user(user):
    db.session.add(user)
    db.session.commit()


# todo: check, not working
def update_email(user, new_email):
    user.email = new_email
    db.session.commit()

# todo: check, not working
def delete_by_email(email):
    to_delete = Users.query.filter_by(email=email)
    for usr in to_delete:
        usr.delete()


############################## Database classes ###################################################

class Users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100))
    email = db.Column('email', db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


def add_new_user(name, email, password):
    user = Users(name, email, password)
    add_user(user)
    return user


def search_user(name, email):
    found = Users.query.filter_by(email=email).first()
    if found:
        return True
    found = Users.query.filter_by(name=name).first()
    return found


# todo: check if db.commit() works
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


def all_users():
    return Users.query.all()
