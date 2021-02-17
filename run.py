from WebDomains import app, db

if __name__ == '__main__':
    # it creates the database if it does not exists
    db.create_all()
    app.run(debug=True)

'''
how to modify an html file with python
using React and JS
add an option of change password or email or username

'''
