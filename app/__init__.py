from flask import Flask


def create_app():

	app = Flask(__name__)

	app.config.from_object('config')

	from . import index, register, models

	models.init_app(app)
	app.register_blueprint(register.register_bp)
	app.register_blueprint(index.index_bp)


	return app
