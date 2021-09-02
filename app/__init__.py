from flask import Flask

# TODO : add logging
# TODO : fix UI

def create_app():

	app = Flask(__name__)

	app.config.from_object('config')

	from . import index, register, models

	models.init_app(app)
	app.register_blueprint(register.register_bp)
	app.register_blueprint(index.index_bp)


	return app
