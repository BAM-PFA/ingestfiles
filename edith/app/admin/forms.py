from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Department, User, Data_Source, Metadata_Field


class DepartmentForm(FlaskForm):
	"""
	Form for admin to add or edit a department
	"""
	deptname = StringField('Department name', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])
	submit = SubmitField('Submit')

class AddUserForm(FlaskForm):
	"""
	Form for admin to create users
	"""
	department_id = QuerySelectField(
		query_factory=lambda: Department.query.all(),
		get_pk=lambda x: x.id,
		get_label="deptname",
		allow_blank=True,
		blank_text=''
		)
	email = StringField('email address', validators=[DataRequired(),Email()])
	username = StringField('username', validators=[DataRequired()])
	first_name = StringField('First name', validators=[DataRequired()])
	last_name = StringField('Last name', validators=[DataRequired()])
	RSusername = StringField('ResourceSpace username', validators=[DataRequired()])
	RSkey = StringField('ResourceSpace API key', validators=[DataRequired()])
	is_admin = BooleanField('Admin?')
	password = PasswordField('Password', validators=[EqualTo('confirm_password')])
	confirm_password = PasswordField('Confirm Password')

	submit = SubmitField('Submit')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email is already in use.')

class EditUserForm(FlaskForm):
	"""
	Form for admin to create or edit users
	Had to create a separate form to avoid the validate_email method above, 
	otherwise editing an existing user will fail. 
	There's a better way to do it I know but I;m in a hurry. :/
	"""
	department_id = QuerySelectField(
		query_factory=lambda: Department.query.all(),
		get_pk=lambda x: x.id,
		get_label="deptname",
		allow_blank=True,
		blank_text=u'Select a department'
		)
	email = StringField('email address', validators=[DataRequired(),Email()])
	username = StringField('username', validators=[DataRequired()])
	first_name = StringField('First name', validators=[DataRequired()])
	last_name = StringField('Last name', validators=[DataRequired()])
	RSusername = StringField('ResourceSpace username', validators=[DataRequired()])
	RSkey = StringField('ResourceSpace API key', validators=[DataRequired()])
	is_admin = BooleanField('Admin?')
	password = PasswordField('Password', validators=[EqualTo('confirm_password')])
	confirm_password = PasswordField('Confirm Password')

	submit = SubmitField('Submit')

class DataSourceForm(FlaskForm):
	"""
	Form for admin to create or edit metadata source
	"""
	dbName = StringField('Database name', validators=[DataRequired()])
	fmpLayout = StringField('FileMaker Layout name')
	IPaddress = StringField('IP Address', validators=[DataRequired()])
	namespace = StringField('Namespace for XML/XPATH queries')
	username = StringField("Database user's username", validators=[DataRequired()])
	credentials = StringField('Database user password', validators=[DataRequired()])
	description = StringField('Database description')
	primaryAssetID = StringField('Field name for primary ID of an asset')
	secondaryAssetID = StringField('Field name for secondary ID of an asset')
	tertiaryAssetID = StringField('Field name for tertiary ID of an asset')

	submit = SubmitField('Submit')

class MetadataFieldForm(FlaskForm):
	"""
	Form for admin to create or edit metadata field
	"""
	fieldName = StringField('Field display name', validators=[DataRequired()])
	fieldUniqueName = StringField('Unique name for system', validators=[DataRequired()])
	fieldSourceName = StringField('Name of field in source as applicable')
	fieldCategory = StringField(
			'Category field belongs to. Please choose '\
			'"Event","Communications", "Film Collection", or "General".')
	dataSource_id = QuerySelectField(
		query_factory=lambda: Data_Source.query.all(),
		get_pk=lambda x: x.id,
		get_label="dbName",
		allow_blank=True,
		blank_text=u'Select a data source'
		)
	rsFieldID = StringField("ResourceSpace reference ID for field",validators=[DataRequired()])
	description = StringField('Database description')

	submit = SubmitField('Submit')