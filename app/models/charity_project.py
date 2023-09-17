from sqlalchemy import Column, String, Text

from app.models.base import DonationCharityModel


class CharityProject(DonationCharityModel):
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'< name={self.name}, '
            f'description={self.description} >'
            f'{super().__repr__()}'
        )
