from flask import redirect, render_template, request, url_for

from app.models.amazon_principle import AmazonPrinciple
from app.models.question import Question
from app.models.story import Story


def render_all():
    if request.method == "POST":
        name = request.form.get("name")
        principle = AmazonPrinciple.query.filter_by(name=name).first()
        if not principle:
            description = request.form.get("description")
            principle = AmazonPrinciple(name=name, description=description)
            principle.save()
    all_principles = AmazonPrinciple.query.all()
    question_counts = {
        principle.id: len(principle.questions) for principle in all_principles
    }
    return render_template(
        "principles.html",
        principles=all_principles,
        question_counts=question_counts,
    )


def render_single(principle_id):
    principle = AmazonPrinciple.query.get(principle_id)
    edited_question_id = None
    if request.method == "POST":
        if request.form.get("add"):
            question_text = request.form.get("question")
            question = Question(
                question=question_text, amazon_principle_id=principle.id
            )
            question.save()
        elif request.form.get("delete"):
            question = Question.query.get(int(request.form.get("question_id")))
            question.delete()
        elif request.form.get("edit"):
            edited_question_id = int(request.form.get("question_id"))
        elif request.form.get("update"):
            question = Question.query.get(int(request.form.get("question_id")))
            question.question = request.form.get("question")
            question.save()
        elif request.form.get("story"):
            story = Story(
                name=request.form.get("name"),
                company=request.form.get("company"),
                year=int(request.form.get("year")),
                situation=request.form.get("situation"),
                task=request.form.get("task"),
                action=request.form.get("action"),
                result=request.form.get("result"),
                notes=request.form.get("notes"),
            )
            story.save()

    questions = principle.questions
    stories = Story.query.all()
    story_count = len(stories)
    return render_template(
        "principle.html",
        principle=principle,
        questions=questions,
        edited_question_id=edited_question_id,
        stories=stories,
        story_count=story_count,
        story_columns=10,
    )
