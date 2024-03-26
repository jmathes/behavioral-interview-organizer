from pprint import pprint

from flask import redirect, render_template, request, url_for

from app.models.amazon_principle import AmazonPrinciple
from app.models.question import Question
from app.models.story import Story
from app.models.story_applicability import StoryApplicibility


def render_all():
    all_questions = sorted(Question.query.all(), key=lambda q: q.principle.name)
    return render_template(
        "questions.html",
        all_questions=all_questions,
    )


def render_single(question_id):
    question = Question.query.get(question_id)
    if request.method == "POST":
        if request.form.get("update_ratings"):
            for input in request.form:
                if input.startswith("hidden_applicability_"):
                    story_id = int(input.split("_")[2])
                    applicability = int(request.form.get(input))
                    if applicability < 0:
                        continue
                    story_applicability = StoryApplicibility.query.filter_by(
                        story_id=story_id, question_id=question_id
                    ).first()
                    if story_applicability is None:
                        story_applicability = StoryApplicibility(
                            story_id=story_id, question_id=question_id
                        )
                    story_applicability.percent_applicable = applicability
                    story_applicability.save()
    all_stories = Story.query.all()
    applicabilities = {story.id: story.applicable(question) for story in all_stories}
    applicable_stories = sorted(
        [
            (
                story,
                applicabilities[story.id],
                len([q for q in story.questions_that_need_me if q.id != question_id]),
            )
            for story in all_stories
        ],
        key=lambda pair: (
            -(pair[1]).percent_applicable if pair[1] is not None else -1000
        ),
    )
    needy_competition = {
        story.name: [
            q.question for q in story.questions_that_need_me if q.id != question_id
        ]
        for story in all_stories
    }

    pprint(needy_competition)
    return render_template(
        "question.html", question=question, applicable_stories=applicable_stories
    )
