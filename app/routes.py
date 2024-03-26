from flask import Blueprint, redirect, url_for

from tinker import export_all

export_all()

from app.controllers import cleanup, index, principles, questions, stories

bio_bp = Blueprint("bio", __name__)


@bio_bp.route("/")
def redirect_to_index():
    return redirect(url_for("bio.render_index"))


@bio_bp.route("/index", methods=["GET"])
def render_index():
    return index.render()


@bio_bp.route("/principles", methods=["GET", "POST"])
def render_principles():
    return principles.render_all()


@bio_bp.route("/principles/<principle_id>", methods=["GET", "POST"])
def render_principle(principle_id):
    return principles.render_single(principle_id)


@bio_bp.route("/stories", methods=["GET", "POST"])
def render_stories():
    return stories.render_all()


@bio_bp.route("/stories/<story_id>", methods=["GET", "POST"])
def render_story(story_id):
    return stories.render_single(story_id)


@bio_bp.route("/questions", methods=["GET", "POST"])
def render_questions():
    return questions.render_all()


@bio_bp.route("/questions/<question_id>", methods=["GET", "POST"])
def render_question(question_id):
    return questions.render_single(question_id)


@bio_bp.route("/cleanup", methods=["GET"])
def render_cleanup():
    return cleanup.render()
