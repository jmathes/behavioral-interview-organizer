import app.models.story_applicability
from app.models.base_model import Column, ForeignKey, Integer, Model, String


class Story(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    company = Column(String(80), unique=False, nullable=False)
    year = Column(Integer, unique=False, nullable=True)
    situation = Column(String(), unique=False, nullable=False)
    task = Column(String(), unique=False, nullable=False)
    action = Column(String(), unique=False, nullable=False)
    result = Column(String(), unique=False, nullable=False)
    notes = Column(String(), unique=False, nullable=False)

    def __repr__(self):
        return f"<Story situation='{self.situation}' task='{self.task}' action='{self.action}' result='{self.result}' notes='{self.notes}'>"

    def applicable(self, question):
        return app.models.story_applicability.StoryApplicibility.query.filter_by(
            story_id=self.id, question_id=question.id
        ).first()

    @property
    def questions_that_need_me(self):
        all_applicabilities = (
            app.models.story_applicability.StoryApplicibility.query.filter_by(
                story_id=self.id
            ).all()
        )
        high_applicabilities = [
            applicability
            for applicability in all_applicabilities
            if applicability.percent_applicable >= 80
        ]
        lonely_questions = [
            applicability.question
            for applicability in high_applicabilities
            if len(applicability.question.good_answers) == 1
        ]
        return lonely_questions
