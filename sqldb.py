# import os
# from flask_sqlalchemy import SQLAlchemy
# from run import app

# basedir = os.path.abspath(os.path.dirname(__file__))

# # app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# #creating model aka table
# class Student_details(db.Model):

#     __tablename__ = 'students'

#     regnumber = db.Column(db.Text, primary_key=True)
#     firstname = db.Column(db.Text)
#     lastname = db.Column(db.Text)
#     level = db.Column(db.Integer)
#     department = db.Column(db.Text)

#     def __init__(self, regnumber, firstname, lastname, level, department):
#         self.regnumber = regnumber
#         self.firstname = firstname
#         self.lastname = lastname
#         self.level = level
#         self.department = department

#     def __repr__(self):
#         return f"{self.regnumber}, {self.firstname}, {self.lastname}, {self.level}, {self.department}"

import os
from flask import render_template, url_for, redirect, flash
from runapp import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from form import AddForm, DelForm

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'thisissupposedtobeasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


#creating model aka table
class Student_details(db.Model):

    __tablename__ = 'students'

    regnumber = db.Column(db.Text, primary_key=True)
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)
    level = db.Column(db.Integer)
    department = db.Column(db.Text)

    def __init__(self, regnumber, firstname, lastname, level, department):
        self.regnumber = regnumber
        self.firstname = firstname
        self.lastname = lastname
        self.level = level
        self.department = department

    def __repr__(self):
        return f"{self.regnumber}, {self.firstname}, {self.lastname}, {self.level}, {self.department}"



#view functions for the forms
@app.route('/form')
def index():
    return render_template('formhome.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():

    form = AddForm()

    if form.validate_on_submit():
        regnumber = form.regnumber.data
        firstname = form.firstname.data.capitalize()
        lastname = form.lastname.data.capitalize()
        level = form.level.data
        department = form.department.data.capitalize()

        newreg = Student_details(regnumber, firstname, lastname, level, department)

        db.session.add(newreg)
        db.session.commit()

        flash('Student added successfully!')
        return redirect(url_for('list_students'))

    return render_template('addform.html', form=form)


@app.route('/list')
def list_students():

    students = Student_details.query.all()
    return render_template('listform.html', students=students)


@app.route('/delete', methods=['GET', 'POST'])
def del_student():

    form = DelForm()

    if form.validate_on_submit():
        regnumber = form.regnumber.data
        student = Student_details.query.get(regnumber)
        db.session.delete(student)
        db.session.commit()

        return redirect(url_for('list_students'))
    return render_template('delete.html', form=form)






if __name__ == '__main__':
    app.run(debug=True)

