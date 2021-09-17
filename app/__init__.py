from flask import Flask


def create_app():

	app = Flask(__name__, instance_relative_config=True)

	app.config.from_object('config')
	app.config.from_pyfile('config.py') #load instance specific config file

	from . import index, register, models, email

	models.init_app(app)
	email.init_app(app)
	app.register_blueprint(register.register_bp)
	app.register_blueprint(index.index_bp)


	return app
