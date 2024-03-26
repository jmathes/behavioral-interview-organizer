from flask import redirect, render_template, request, url_for

from app.models.amazon_principle import AmazonPrinciple
from app.models.question import Question
from app.models.story import Story
from app.models.story_applicability import StoryApplicibility


def render():
    all_applicabilities = StoryApplicibility.query.all()
    for applicability in all_applicabilities:
        if applicability.story is None or applicability.question is None:
            applicability.delete()

    all_stories = Story.query.all()
    all_questions = Question.query.all()
    all_associations = StoryApplicibility.query.all()
    associations_by_relations = {
        (association.story_id, association.question_id)
        for association in all_associations
    }
    story_missing_association_counts = {
        story: len(
            [
                question
                for question in all_questions
                if (story.id, question.id) not in associations_by_relations
            ]
        )
        for story in all_stories
    }
    question_missing_association_counts = {
        question: len(
            [
                story
                for story in all_stories
                if (story.id, question.id) not in associations_by_relations
            ]
        )
        for question in all_questions
    }

    lonely_stories = [
        (story, count)
        for story, count in story_missing_association_counts.items()
        if count > 0
    ]
    lonely_questions = [
        (question, count)
        for question, count in question_missing_association_counts.items()
        if count > 0
    ]
    unfinished_stories = [
        story
        for story in all_stories
        if any(
            len(field.strip()) < 5
            for field in [
                story.situation,
                story.task,
                story.action,
                story.result,
                story.notes,
            ]
        )
    ]
    unanswred_questions = [
        question for question in all_questions if len(question.good_answers) == 0
    ]
    underanswered_questions = [
        question for question in all_questions if len(question.good_answers) == 1
    ]
    for question in underanswered_questions:
        print("Underanswered question: ", question.question)
        print("Good answers len:", len(question.good_answers))
        print("Good answers directly:", question.good_answers)
    cleanup_length = max(
        len(lonely_stories),
        len(lonely_questions),
        len(unfinished_stories),
        len(unanswred_questions),
        len(underanswered_questions),
    )

    return render_template(
        "cleanup.html",
        lonely_stories=lonely_stories,
        lonely_questions=lonely_questions,
        unfinished_stories=unfinished_stories,
        unanswred_questions=unanswred_questions,
        underanswered_questions=underanswered_questions,
        cleanup_length=cleanup_length,
    )
