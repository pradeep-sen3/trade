from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from include.models import User


class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=5, max=40)])
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label = 'Register')

    # According to flask documentation, to add your own validators use the following template.
    '''
    def validate_field(self, field):
        validate the field
        if a validation error occurs:
            raise exception
    '''

    def validate_username(self, username):
        # If a user with the given username already exists, than raise an exception.
        user = User.query.filter_by(username = username.data).first()
        # SQL equivalent:
        # SELECT * FROM user
        # WHERE self.username = username
        # LIMIT 1
        if user:
            raise ValidationError('username taken!')

    def validate_email(self, email):
        # If a user with the given email already exists, than raise an exception.
        user = User.query.filter_by(email = email.data).first()
        # SQL equivalent:
        # SELECT * FROM user
        # WHERE self.email = email
        # LIMIT 1
        if user:
            raise ValidationError('An account with this email already exists!')


class LoginForm(FlaskForm):
    email = StringField()
    password = PasswordField()
    remember = BooleanField('Remember Me')
    submit = SubmitField(label = 'Log In')


class PurchaseForm(FlaskForm):
    shares = StringField()
    submit = SubmitField(label = 'Buy')

    def validate_shares(self, shares):
        if not shares.data.isdigit():
            raise ValidationError('Number of shares must be a positive number!')
        if int(shares.data) <= 0:
            raise ValidationError('Number of shares must be at least 1.')


class SellForm(FlaskForm):
    shares = StringField()
    submit = SubmitField(label = 'Sell')

    def validate_shares(self, shares):
        if not shares.data.isdigit():
            raise ValidationError('Number of shares must be a positive number!')
        if int(shares.data) <= 0:
            raise ValidationError('Number of shares must be at least 1.')
