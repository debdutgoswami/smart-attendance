import graphene
from graphene_django.debug import DjangoDebug
from .authentication.schema import UserQuery, UserMutation


class Query(UserQuery):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(UserMutation):
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query, mutation=Mutation)