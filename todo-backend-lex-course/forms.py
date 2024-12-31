from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, DataRequired

# class LoginForm(FlaskForm):
#     login_name = StringField("User Name", validators = [InputRequired()] )
#     login_password = PasswordField("Password", validators = [InputRequired()])
#     # description = TextAreaField('Description', validators=[DataRequired()])
#     login_submit = SubmitField("Login")
    
class LoginForm(FlaskForm):
    login_name = StringField("User Name", validators = [InputRequired()], render_kw = {"placeholder": "User Name", "class": "inputfield"} )
    login_password = PasswordField("Password", validators = [InputRequired()], render_kw = {"placeholder": "Password", "class": "inputfield"} )
    login_submit = SubmitField("Login", render_kw ={"class": "registerBtn"})

