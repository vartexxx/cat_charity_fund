from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import AbstractModel


class Donation(AbstractModel):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
