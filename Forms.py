from wtforms import Form, RadioField, TextAreaField, SelectField, StringField, IntegerField, PasswordField, validators
from wtforms.fields import TimeField, DateField, EmailField
from wtforms.validators import DataRequired


class CreateFeedbackForm(Form):
    ratings = RadioField('Rating',
                         choices=[('1', 'Very unsatisfied'), ('2', 'Unsatisfied'), ('3', 'Neutral'), ('4', 'Satisfied'),
                                  ('5', 'Very Satisfied')],
                         default='F',
                         )
    remarks = TextAreaField('Feedback, if any', [validators.Optional()])


class CreateProductForm(Form):
    first_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Product Description', [validators.Length(min=1, max=1500), validators.DataRequired()])
    price = StringField('Price', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Promotion', [validators.DataRequired()],
                         choices=[('', 'Select'), ('Yes', 'Available'), ('No', 'Unavailable')], default='')
    membership = RadioField('Company', choices=[('A', 'ANIPLEX'), ('H', 'Hakken'), ('LT', 'La Tendos')], default='F')
    remarks = SelectField('Category', [validators.DataRequired()],
                          choices=[('B', 'Best Selling'), ('P', 'Price'), ('New', 'New Arrival'), ('N', 'Nendoroids'),
                                   ('F', 'Figurines')])


class CreateCartForm(Form):
    first_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Product Description', [validators.Length(min=1, max=1500), validators.DataRequired()])
    price = StringField('Price', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Promotion', [validators.DataRequired()],
                         choices=[('', 'Select'), ('Yes', 'Available'), ('No', 'Unavailable')], default='')
    membership = RadioField('Company', choices=[('A', 'ANIPLEX'), ('H', 'Hakken'), ('LT', 'La Tendos')], default='F')
    remarks = SelectField('Category', [validators.DataRequired()],
                          choices=[('B', 'Best Selling'), ('P', 'Price'), ('New', 'New Arrival'), ('N', 'Nendoroids'),
                                   ('F', 'Figurines')])


class CreateArtForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('E-mail', [validators.DataRequired(), validators.Email()])
    phone = StringField('Phone Number', [validators.Length(min=8, max=8), validators.DataRequired()])
    age = IntegerField('Age', [validators.NumberRange(min=1, max=99), validators.DataRequired()])
    gender = RadioField('Gender', choices=[('M', 'Male'), ('F', 'Female')], default='')
    sname = StringField('Name of Submission', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreatePostForm(Form):
    dname = StringField('Display Name', [validators.Length(min=1, max=20), validators.DataRequired()])
    caption = StringField('Caption', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = EmailField('E-mail', [validators.Email(), validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])
    profileuser = ""


class CreateEnquiryForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('E-mail', [validators.Length(min=6, max=35), validators.DataRequired()])
    topic = SelectField('Topic', [validators.DataRequired()],
                        choices=[('', 'Select'), ('Collaboration', 'Collaboration'), ('Sponsorship', 'Sponsorship'),
                                 ('Performance', 'Performance'), ('Report', 'Report'), ('Other', 'Other')], default='')
    enquirys = TextAreaField('Enquiry', [validators.Optional()])


class CreateEventForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=150), validators.DataRequired()])
    date = DateField("Date", [validators.DataRequired()], format='%Y-%m-%d')
    starttime = TimeField('Start', validators=[DataRequired()])
    endtime = TimeField('End', validators=[DataRequired()])
    url = StringField('URL', [validators.Length(min=1, max=150), validators.DataRequired()])


class AdminLoginForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])
    profileuser = ""


class CreateAdminForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = EmailField('E-mail', [validators.Email(), validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])
