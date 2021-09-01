from flask import request, Blueprint

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
	print(request.form)
	return 'Great success!' 