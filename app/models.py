import csv
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db_cli = AppGroup('db')

class Team(db.Model):

	__tablename__ = 'teams'

	id = db.Column(db.Integer, db.Sequence('team_id_seq'), primary_key=True)
	name = db.Column(db.String, nullable=False)
	project_title = db.Column(db.String, nullable=True)
	size = db.Column(db.Integer, nullable=False)
	proposal_url = db.Column(db.String(100), nullable=True)


	def __repr__(self):
		return f'<Team(name=\'{self.name}\', project_title=\'{self.project_title}\', size=\'{self.size}\'), proposal_url=\'{self.proposal_url}\'>'

class Participant(db.Model):

	__tablename__ = 'participants'

	id = db.Column(db.Integer, db.Sequence('participants_id_seq'), primary_key=True)
	team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

	name = db.Column(db.String, nullable=False)
	roll_no = db.Column(db.String(7), nullable=False)
	email = db.Column(db.String, nullable=False)
	phone_no = db.Column(db.String(11), nullable=False)
	team = db.relationship("Team", back_populates="participants")

	def __repr__(self):
		return f'<Participant(name=\'{self.name}\', roll_no=\'{self.roll_no}\', email=\'{self.email}\', phone_no=\'{self.phone_no}\')>'

Team.participants = db.relationship("Participant", order_by=Participant.id, back_populates="team")

def init_app(app):

	db.init_app(app)
	app.cli.add_command(db_cli)

	with app.app_context():
		db.create_all()
		db.session.commit()
	

def add_team(team:Team):
	
	db.session.add(team)
	db.session.commit()

def add_proposal(team_name:str, project_title:str, proposal_url:str):

	team = db.session.query(Team).filter_by(name = team_name).scalar()

	if team is None:
		return False

	team.project_title = project_title
	team.proposal_url = proposal_url
	db.session.commit()

	return True


def team_exists(team_name:str) -> bool:

	team = db.session.query(Team).filter(Team.name == team_name)
	return db.session.query(team.exists()).scalar()


@db_cli.command('dump')
def _dump_db():

	with open('db_participants_dump.csv', mode='w', newline='') as csv_file:

		fieldnames = [ 'team_name', 'partcipant_name', 'partcipant_roll_no', 'partcipant_email', 'partcipant_no',]
		writer = csv.DictWriter(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames, dialect='excel')

		writer.writeheader()

		[ 
			[ _write_participant(writer, p) for p in team.participants ] 
			for team in db.session.query(Team).all()
		]

	with open('db_teams_dump.csv', mode='w', newline='') as csv_file:

		fieldnames = ['team_name', 'project_title', 'size', 'proposal_url',]
		writer = csv.DictWriter(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)

		writer.writeheader()

		[
			_write_team(writer, team)
			for team in db.session.query(Team).all()
		]

def _write_participant(writer, p):
	writer.writerow({
		'team_name': p.team.name,
		'partcipant_name': p.name, 
		'partcipant_roll_no': p.roll_no, 
		'partcipant_email': p.email, 
		'partcipant_no': p.phone_no
		})

def _write_team(writer, t):
	writer.writerow({
		'team_name': t.name,
		'project_title': t.project_title,
		'size': t.size,
		'proposal_url': t.proposal_url
		})

@db_cli.command('erase')
def _erase_db():

	answer = input('\nEnter "Delete all data from database 5436**" to delete all data from database : ')

	if answer == 'Delete all data from database 5436**':

		db.session.query(Team).delete()
		db.session.query(Participant).delete()
		db.session.commit()

		print('Database erased completely')
	
	else:

		print('Phrase entered doesn\'t match the one provided. Database deletion canceled')
