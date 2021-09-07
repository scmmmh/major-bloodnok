"""Database model for account categories."""
from sqlalchemy import Column, Integer, String, ForeignKey

from .meta import Base


class Category(Base):
    """Transaction model class."""

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    title = Column(String(255))

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
