from sqlalchemy import create_engine, Column, String, Integer, Sequence
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
Session = sessionmaker()
session = None
engine = create_engine('sqlite:///register.db', echo=True)


class Team(Base):

	__tablename__ = 'teams'

	id = Column(Integer, Sequence('team_id_seq'), primary_key=True)
	name = Column(String)
	project_title = Column(String)
	size = Column(Integer)

	def __repr__(self):
		return f'<Team(name=\'{self.name}\', project_title=\'{self.project_title}\', size=\'{self.size}\')>'

def init_app(app):

	global session

	Session.configure(bind=engine)
	Base.metadata.create_all(engine)
	session = Session()

def add_team(name:str, project_title:str, size:int, commit=True):
	
	session.add(Team(name=name, project_title=project_title, size=size))

	if commit:
		session.commit()