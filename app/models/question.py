import app.models.amazon_principle
from app.models.base_model import Column, ForeignKey, Integer, Model, String


class Question(Model):
    id = Column(Integer, primary_key=True)
    question = Column(String(1024), unique=True, nullable=False)
    amazon_principle_id = Column(
        Integer, ForeignKey("amazon_principle.id"), nullable=False
    )

    def __repr__(self):
        return f"<Question {self.question}>"

    @property
    def principle(self):
        return app.models.amazon_principle.AmazonPrinciple.query.get(
            self.amazon_principle_id
        )

    def applicable(self, story):
        return app.models.story_applicability.StoryApplicibility.query.filter_by(
            story_id=story.id, question_id=self.id
        ).first()

    @property
    def good_answers(self):
        return [
            applicability.story
            for applicability in app.models.story_applicability.StoryApplicibility.query.filter_by(
                question_id=self.id
            ).all()
            if applicability.percent_applicable >= 80
        ]
