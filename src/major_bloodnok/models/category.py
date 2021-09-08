"""Database model for account categories."""
import json

from sqlalchemy import Column, Integer, String, ForeignKey

from .meta import Base


class Category(Base):
    """Transaction model class."""

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    title = Column(String(255))

    @classmethod
    def from_jsonapi(cls, body):
        data = json.loads(body)
        obj = Category(title=data['attributes']['title'])
        if 'relationships' in data and 'parent' in data['relationships']:
            obj.parent_id = data['relationships']['parent']['data']['id']
        return obj

    def update(self, new_obj):
        self.title = new_obj.title
        self.parent_id = new_obj.parent_id

    def jsonapi(self):
        """Return the Transaction in JSONAPI format."""
        obj = {
            'type': 'categories',
            'id': str(self.id),
            'attributes': {
                'title': self.title
            },
            'relationships': {
            }
        }
        if self.parent_id is not None:
            obj['relationships']['parent'] = {
                'data': {
                    'type': 'categories',
                    'id': str(self.parent_id)
                }
            }
        return obj
