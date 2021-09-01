from flask import request, Blueprint
from .models import add_team

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():

	add_team(
		name=request.form['teamName'],
		project_title=request.form['projectTitle'],
		size=int(request.form['teamSize'])
		)

	return 'Great success!' 