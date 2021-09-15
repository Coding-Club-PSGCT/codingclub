import os
from flask import request, Blueprint, redirect, current_app, render_template
from .models import Team, Participant, add_team, team_exists, add_proposal
from .email import send_registration_email, validate_emails
from uuid import uuid4

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():

	if request.method == 'GET':
		return render_template('register.html')

	
	team = Team(
		name=request.form['teamName'],
		size=int(request.form['teamSize']),
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

	try:
		validate_emails(team)
		send_registration_email(team)
	except Exception as e:
		current_app.logger.warning('Error while sending registration email : %s', e)
		return render_template('register.html', error_msg='Email verification failed. Ensure you have entered the official college email with no typos')

	add_team(team)

	return redirect('/')

@register_bp.route('/upload_proposal', methods=['GET', 'POST'])
def upload_proposal():

	if request.method == 'GET':
		return render_template('upload_proposal.html', error_msg={})
	
	#Check if user has uploaded proposal file
	if 'proposal' not in request.files or request.files['proposal'].filename == '':
		return  render_template('upload_proposal.html', error_msg={'file':'Please go back and upload proposal!'})
	
	if not team_exists(request.form['teamName']):
		return render_template('upload_proposal.html', error_msg={'team_name':'Team does not exist'})

	file_url = save_file(
		current_app.config['UPLOADS_DIR'], 
		request.files['proposal']
		)
	
	success = add_proposal(
		team_name = request.form['teamName'],
		project_title = request.form['projectTitle'],
		proposal_url = file_url
	)

	if not success:
		return render_template('upload_proposal.html', error_msg={'file':'Error while uploading proposal. Please upload proposal again'})
	
	return redirect('/')


def save_file(uploads_folder, file):

	ext =  file.filename.rsplit('.', 1)[-1].lower()
	rand_file_name = str(uuid4())
	filename = os.path.join(uploads_folder, f'{rand_file_name}.{ext}')

	file.save(filename)

	return f'/static/uploads/{rand_file_name}.{ext}'


