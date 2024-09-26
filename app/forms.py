from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TimeField, SelectField, FieldList, FormField, FileField, PasswordField, DateField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddCupForm(FlaskForm):
    name = StringField('Cup Name', validators=[DataRequired()])
    submit = SubmitField('Add Cup')

class AddCompetitionForm(FlaskForm):
    name = StringField('Competition Name', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', format='%H:%M', validators=[DataRequired()])  # Added start time
    poster = StringField('Poster URL')
    cup_id = SelectField('Cup', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Competition')

class PigeonLandingTimeForm(FlaskForm):
    landing_time = TimeField('Landing Time', format='%H:%M', validators=[Optional()])

class ParticipantForm(FlaskForm):
    name = StringField('Participant Name', validators=[DataRequired()])
    profile_pic = FileField('Profile Picture', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'])])
    landing_times1 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times2 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times3 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times4 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times5 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times6 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times7 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times8 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times9 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times10 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times11 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times12 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    
class AddResultsForm(FlaskForm):
    competition_id = SelectField('Competition', coerce=int)
    participants = FieldList(FormField(ParticipantForm), min_entries=1)
    submit = SubmitField('Add Results')

class EditParticipantForm(FlaskForm):
    name = StringField('Participant Name', validators=[DataRequired()])
    profile_pic = FileField('Profile Picture', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'])])
    landing_times1 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times2 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times3 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times4 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times5 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times6 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times7 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times8 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times9 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times10 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times11 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    landing_times12 = TimeField('Landing Time', format='%H:%M', validators=[Optional()])
    submit = SubmitField('Update Participant')
    
    
