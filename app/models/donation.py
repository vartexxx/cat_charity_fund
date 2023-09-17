from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import DonationCharityModel


class Donation(DonationCharityModel):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return (
            f'< comment={self.comment}, '
            f'user_id={self.user_id} >'
            f'{super().__repr__()}'
        )
