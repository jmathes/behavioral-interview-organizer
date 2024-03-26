from flask import redirect, render_template, request, url_for

from app.models.amazon_principle import AmazonPrinciple
from app.models.question import Question
from app.models.story import Story
from app.models.story_applicability import StoryApplicibility


def render():
    return render_template(
        "index.html",
    )
