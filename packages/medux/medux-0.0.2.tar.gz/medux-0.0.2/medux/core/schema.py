import graphene
from .models import User
from graphene_django import DjangoObjectType

from gdaps.graphene.api import IGrapheneSchema


class UserType(DjangoObjectType):
    """MedUX's built-in User type"""

    class Meta:
        model = User


class UserQuery:
    users = graphene.List(UserType)

    @staticmethod
    def resolve_users(self, info, **kwargs):
        return User.objects.all()


# Here comes the magic:
class UserSchema(IGrapheneSchema):
    query = UserQuery
