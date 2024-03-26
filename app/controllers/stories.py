from flask import redirect, render_template, request, url_for

from app.models.amazon_principle import AmazonPrinciple
from app.models.question import Question
from app.models.story import Story
from app.models.story_applicability import StoryApplicibility


def render_single(story_id):
    story = Story.query.get(story_id)
    if request.method == "POST":
        if request.form.get("update"):
            try:
                story.year = int(request.form.get("year").strip())
            except:
                story.year = None
            story.situation = request.form.get("situation").strip()
            story.task = request.form.get("task").strip()
            story.action = request.form.get("action").strip()
            story.result = request.form.get("result").strip()
            story.notes = request.form.get("notes").strip()
            story.save()
        elif request.form.get("delete"):
            applicabilities_for_story = StoryApplicibility.query.filter_by(
                story_id=story_id
            ).all()
            for applicability in applicabilities_for_story:
                applicability.delete()
            story.delete()
            return redirect(url_for("bio.render_stories"))
        elif request.form.get("update_ratings"):
            for input in request.form:
                if input.startswith("hidden_applicability_"):
                    applicability = int(request.form.get(input))
                    if applicability < 0:
                        continue
                    question_id = int(input.split("_")[2])
                    story_applicability = StoryApplicibility.query.filter_by(
                        story_id=story_id, question_id=question_id
                    ).first()
                    if story_applicability is None:
                        story_applicability = StoryApplicibility(
                            story_id=story_id, question_id=question_id
                        )
                    story_applicability.percent_applicable = applicability
                    story_applicability.save()

    all_questions = Question.query.all()
    applicabilities = {
        question.id: story.applicable(question) for question in all_questions
    }
    quetions_that_need_me = set()
    for question_id in applicabilities:
        if applicabilities[question_id] is not None:
            if 0 > applicabilities[question_id].percent_applicable:
                applicabilities[question_id].percent_applicable = 0
                applicabilities[question_id].save()
            if 100 < applicabilities[question_id].percent_applicable:
                applicabilities[question_id].percent_applicable = 100
                applicabilities[question_id].save()
            if applicabilities[question_id].percent_applicable >= 80:
                question = Question.query.get(question_id)
                assert len(question.good_answers) >= 1
                if len(question.good_answers) == 1:
                    quetions_that_need_me.add(question)
    applicable_questions = sorted(
        [(question, applicabilities[question.id]) for question in all_questions],
        key=lambda pair: (
            -(pair[1]).percent_applicable if pair[1] is not None else -1000
        ),
    )

    return render_template(
        "story.html",
        story=story,
        question_count=len(all_questions),
        applicable_questions=applicable_questions,
        quetions_that_need_me=quetions_that_need_me,
    )


def render_all():
    all_stories = Story.query.all()
    print(all_stories)
    return render_template("stories.html", stories=all_stories)
