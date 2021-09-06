"""Database model for account categorisation rules."""
from sqlalchemy import Column, Integer, String, ForeignKey

from .meta import Base


class Rule(Base):
    """Rule model class."""

    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    description = Column(String(255))
    direction = Column(String(255))

    def jsonapi(self):
        """Return the Rule in JSONAPI format."""
        return {
            'type': 'rules',
            'id': str(self.id),
            'attributes': {
                'date': self.description,
                'direction': self.direction
            },
            'relationships': {
                'category': {
                    'data': {
                        'type': 'categories',
                        'id': str(self.category_id)
                    }
                }
            }
        }
