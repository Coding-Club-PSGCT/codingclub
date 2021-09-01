from flask import Flask

def create_app():

	app = Flask(__name__)

	app.config.from_object('config')

	from . import register

	app.register_blueprint(register.register_bp)

	return app