"""Database model for account categorisation rules."""
import json

from sqlalchemy import Column, Integer, String, ForeignKey

from .meta import Base


class Rule(Base):
    """Rule model class."""

    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    description = Column(String(255))
    direction = Column(String(255))

    @classmethod
    def from_jsonapi(cls, body):
        data = json.loads(body)
        return Rule(description=data['attributes']['pattern'],
                    direction=data['attributes']['direction'],
                    category_id=data['relationships']['category']['data']['id'])

    def jsonapi(self):
        """Return the Rule in JSONAPI format."""
        return {
            'type': 'rules',
            'id': str(self.id),
            'attributes': {
                'pattern': self.description,
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
