
from flask import render_template, url_for, request, redirect
from models import db, Project, app
import datetime
import csv


current_projects = []


def initialize_projects():
    if len(current_projects) == 0:
        with open('backup.csv') as csv_file:
            projects = csv.DictReader(csv_file, delimiter='#')
            for project in projects:
                title = project["title"]
                completion_date = datetime.datetime.strptime(
                    project["date"], "%Y-%m")
                description = project["desc"]
                skills = project["skills"]
                github_link = project["github"]
                new_project = Project(
                        title=title,
                        completion_date=completion_date,
                        description=description,
                        skills=skills,
                        github_link=github_link
                    )
                db.session.add(new_project)
            db.session.commit()


def format_project(project, dateformat="%Y-%m"):
    format_project = {}
    format_project["id"] = project.id
    format_project["title"] = project.title
    format_project["date"] = datetime.datetime.strftime(
        project.completion_date, dateformat)
    format_project["desc"] = project.description
    format_project["skills"] = [skill for skill in project.skills.split(",")]
    format_project["github"] = project.github_link

    return format_project


def get_project(id):
    return Project.query.get_or_404(id)


def get_current_projects():
    projects = Project.query.order_by(Project.id).all()
    current_projects.clear()
    for project in projects:
        current_projects.append(format_project(project))


@app.route("/")
def index():
    return render_template("index.html", projects=current_projects)


@app.route("/about")
def about():
    return render_template("about.html", projects=current_projects)


@app.route("/projects/<id>")
def view_project(id):
    target_project = format_project(get_project(id), dateformat="%B %Y")

    return render_template("detail.html", target_project=target_project,
                           projects=current_projects)


@app.route("/projects/new", methods={"GET", "POST"})
def create_new_project():
    if request.form:
        title = request.form["title"]
        completion_date = datetime.datetime.strptime(
            request.form["date"], "%Y-%m")
        description = request.form["desc"]
        skills = request.form["skills"]
        github_link = request.form["github"]
        new_project = Project(
                title=title,
                completion_date=completion_date,
                description=description,
                skills=skills,
                github_link=github_link
            )
        db.session.add(new_project)
        db.session.commit()
        get_current_projects()

        return redirect(url_for("index"))

    return render_template("newproject.html", projects=current_projects)


@app.route("/projects/<id>/edit", methods={"GET", "POST"})
def edit_project(id):
    target_project = get_project(id)
    if request.form:
        target_project.title = request.form["title"]
        target_project.completion_date = datetime.datetime.strptime(
            request.form["date"], "%Y-%m")
        target_project.description = request.form["desc"]
        target_project.skills = request.form["skills"]
        target_project.github_link = request.form["github"]
        db.session.commit()
        get_current_projects()

        return redirect(url_for("view_project", id=id))

    formatted_target_project = format_project(target_project)

    return render_template("editproject.html",
                           target_project=formatted_target_project,
                           projects=current_projects)


@app.route("/projects/<id>/delete")
def delete_project(id):
    target_project = get_project(id)
    db.session.delete(target_project)
    db.session.commit()
    get_current_projects()

    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', msg=error,
                           projects=current_projects), 404


if __name__ == '__main__':
    db.create_all()
    get_current_projects()
    initialize_projects()
    app.run(debug=True, port=8000, host='127.0.0.1')
