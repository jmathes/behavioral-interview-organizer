import app.models.question
import app.models.story
from app.models.base_model import Column, ForeignKey, Integer, Model


class StoryApplicibility(Model):
    id = Column(Integer, primary_key=True)
    story_id = Column(Integer, ForeignKey("story.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
    percent_applicable = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<StoryApplicibility {self.story_id} {self.percent_applicable}% {self.question_id}>"

    @property
    def question(self):
        return app.models.question.Question.query.get(self.question_id)

    @property
    def story(self):
        return app.models.story.Story.query.get(self.story_id)
