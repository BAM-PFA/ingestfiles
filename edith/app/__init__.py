'''
This is sets up the various objects that are needed to 
run the app. Namely, it creates the config used by the app,
inits the db object we use to interact w the db, and registers
the blueprints used by the various modules.
'''

# Flask imports
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# local imports
from config import app_config

# init a loginManager
login_manager = LoginManager()
# init a DB object
db = SQLAlchemy()

def create_app(config_name):
	# instance_relative_config gets instance-specific config stuff
	app = Flask(__name__, instance_relative_config=True)
	# or really, config_name var should be read from os.getenv, but that's beyond my powers
	app.config.from_object(app_config['production']) 
	app.config.from_pyfile('config.py')

	app.jinja_env.add_extension('jinja2.ext.do')

	# I wish I knew what this does...
	Bootstrap(app)
	# init the db communication... ? 
	db.init_app(app)

	login_manager.init_app(app)
	login_manager.login_message = "You must be logged in to access this page."
	login_manager.login_view = "auth.login"
	migrate = Migrate(app, db)

	from app import models

	from .admin import admin as admin_blueprint
	app.register_blueprint(admin_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .home import home as home_blueprint
	app.register_blueprint(home_blueprint)#, url_prefix='/home')

	from .ingest import ingest as ingest_blueprint
	app.register_blueprint(ingest_blueprint)

	from .lto import lto as lto_blueprint
	app.register_blueprint(lto_blueprint)

	@app.errorhandler(403)
	def forbidden(error):
		return render_template('errors/403.html', title='Forbidden'), 403

	@app.errorhandler(404)
	def page_not_found(error):
		return render_template('errors/404.html', title='Page Not Found'), 404

	@app.errorhandler(500)
	def internal_server_error(error):
		return render_template('errors/500.html', title='Server Error'), 500

	return app
