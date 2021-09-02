from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Team(db.Model):

	__tablename__ = 'teams'

	id = db.Column(db.Integer, db.Sequence('team_id_seq'), primary_key=True)
	name = db.Column(db.String, nullable=False)
	project_title = db.Column(db.String, nullable=False)
	size = db.Column(db.Integer, nullable=False)
	proposal_url = db.Column(db.String(100), nullable=False)


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

	with app.app_context():
		db.create_all()
		db.session.commit()
	

def add_team(team:Team, commit=True):
	
	db.session.add(team)

	if commit:
		db.session.commit()

def get_all():
	return str([ [ p.name for p in team.participants ] for team in db.session.query(Team).all() ])