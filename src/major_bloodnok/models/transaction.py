"""Database model for account transactions."""
from sqlalchemy import Column, Integer, Date, Float, String

from .meta import Base


class Transaction(Base):
    """Transaction model class."""

    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    description = Column(String(255))
    amount = Column(Float)
    direction = Column(String(16))
    initiator = Column(String(255))

    def jsonapi(self):
        """Return the Transaction in JSONAPI format."""
        return {
            'type': 'transactions',
            'id': str(self.id),
            'attributes': {
                'date': self.date.isoformat(),
                'description': self.description,
                'amount': self.amount,
                'direction': self.direction,
                'initiator': self.initiator
            }
        }
