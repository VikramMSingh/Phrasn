from wtforms import *
from flask_wtf import FlaskForm
from flask_wtf import CSRFProtect
from wtforms.validators import DataRequired
from app import app
'''
class LanguageForm(FlaskForm):
    csrf_token=CSRFProtect(app)	
    lang = SelectField('Language', choices=[('en', 'English'), ('es', 'Español'), ('fr', 'Français'), ('de', 'Deutsch'), ('zh', '中文')])

class StdForm(FlaskForm):
    csrf_token=CSRFProtect(app)	
    std = SelectField('Standard', choices=[('Middle School'), ('High School')])
    '''
class LanguageStdForm(FlaskForm):
    lang = SelectField('Language', choices=[
        ('en', 'English'), ('es', 'Español'), ('fr', 'Français'), 
        ('sw', 'Swahili'), ('zh', 'Chinese'), ('hi','Hindi'), 
        ('bn','Bengali'),('ar','Arabic'),('ha','Hausa'),
        ('am','Amharic'),('id', 'Indonesian')], validators=[DataRequired()])
    std = SelectField('Education Level', choices=[
        ('middle_school', 'Middle School'), ('high_school', 'High School'), ('university', 'University')], validators=[DataRequired()])
    submit = SubmitField('Submit')