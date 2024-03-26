from typing import List, Optional

import app.models.question
from app.models.base_model import Column, Integer, Model, String


class AmazonPrinciple(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(120), unique=True, nullable=False)

    def __repr__(self):
        # self._questions = None
        return f"<AmazonPrinciple {self.name}>"

    @property
    def questions(self):
        return app.models.question.Question.query.filter_by(
            amazon_principle_id=self.id
        ).all()
