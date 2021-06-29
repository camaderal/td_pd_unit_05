from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(app)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column('Title', db.String())
    completion_date = db.Column('Completion Date', db.DateTime())
    description = db.Column('Description', db.String())
    skills = db.Column('Skills', db.String())
    github_link = db.Column('Github Link', db.String())

    def __repr__(self):
        return f'''
            \nTitle: {self.title}
            \rCompletion Date: {self.completion_date}
            \rDescription: {self.description}
            \rSkills: {self.skills}
            \rGithub Link: {self.github_link}'''
