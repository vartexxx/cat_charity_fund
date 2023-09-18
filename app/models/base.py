from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean, Integer, CheckConstraint

from app.core.db import Base


class BaseProjectModel(Base):
    __abstract__ = True
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, nullable=True, default=None)
    __table_args___ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount <= full_amount')
    )

    def __repr__(self):
        return (
            f'(full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested}, '
            f'create_date={self.create_date}, '
            f'close_date={self.close_date})'
        )

    @property
    def remaining_amount(self):
        return self.full_amount - self.invested_amount

    def set_fully_invested(self):
        self.invested_amount = self.full_amount
        self.fully_invested = True
        self.close_date = datetime.now()
