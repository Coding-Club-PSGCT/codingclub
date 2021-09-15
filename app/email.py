from flask import render_template
from flask_mail import Mail, Message

mail = Mail()

def send_registration_email(team: 'Team'):
    
    msg = Message(
        'Ideation registration',
        recipients=[p.email for p in team.participants],
        html=render_template('email.html', team_name=team.name, url='codingclub.psgtech.ac.in'),
    )

    mail.send(msg)

def validate_emails(team: 'Team'):
    if not all([ p.email.endswith('@psgtech.ac.in') for p in team.participants]):
        raise Exception('Emails do not end with @psgtech.ac.in')


def init_app(app):

    mail.init_app(app)