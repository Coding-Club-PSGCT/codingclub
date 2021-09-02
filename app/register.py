import os
from flask import request, Blueprint, redirect, current_app, render_template
from .models import Team, Participant, add_team
from uuid import uuid4

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():

	if request.method == 'GET':
		return render_template('register.html')

	if 'proposal' not in request.files:
		return 'Please go back and upload proposal!'

	if request.files['proposal'].filename == '':
		return 'Please go back and upload proposal!'

	file_url = save_file(
		current_app.config['UPLOADS_DIR'], 
		request.files['proposal']
		)

	team = Team(
		name=request.form['teamName'],
		project_title=request.form['projectTitle'],
		size=int(request.form['teamSize']),
		proposal_url=file_url
		)

	team.participants = [
		Participant(
			name=name,
			roll_no=roll_no,
			email=email,
			phone_no=phone_no
			)

		for name, roll_no, email, phone_no 
		in zip(
			request.form.getlist('name'),
			request.form.getlist('rollNo'),
			request.form.getlist('email'),
			request.form.getlist('number')
		)
	]


	add_team(team)
	return redirect('/static/index.html')

def save_file(uploads_folder, file):

	ext =  file.filename.rsplit('.', 1)[-1].lower()
	rand_file_name = str(uuid4())
	filename = os.path.join(uploads_folder, f'{rand_file_name}.{ext}')

	file.save(filename)

	return f'/static/uploads/{rand_file_name}.{ext}'


