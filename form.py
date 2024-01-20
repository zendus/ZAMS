from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators

class AddForm(FlaskForm):
    
    regnumber = StringField('Your Reg Number: ', [validators.Length(min=4, max=13)])

    firstname = StringField('Your Firstname:')

    lastname = StringField('Your Lastname:')

    level = IntegerField('Your level:', [validators.NumberRange(min=0, max=1000, message='Must be an integer with max of 3 numbers')])

    department = StringField('Your Department:')
    
    submit = SubmitField('Click To Submit')


class DelForm(FlaskForm):
    regnumber = StringField('Reg Number of Student to Remove:')
    submit = SubmitField("Remove Student")