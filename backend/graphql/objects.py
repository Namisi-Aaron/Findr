import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import User as UserModel, \
    Profile as ProfileModel, \
    Skill as SkillModel, \
    Blog as BlogModel

class UserObject(SQLAlchemyObjectType):
   user_id = graphene.Int(source='id')

   class Meta:
       model = UserModel
       interfaces = (graphene.relay.Node, )

class BlogObject(SQLAlchemyObjectType):
   blog_id = graphene.Int(source='id')

   class Meta:
       model = BlogModel
       interfaces = (graphene.relay.Node, )       

class ProfileObject(SQLAlchemyObjectType):
   class Meta:
       model = ProfileModel
       interface = (graphene.relay.Node, )

   skills = graphene.List(lambda: SkillObject, name=graphene.String(
   ))

   def resolve_skills(self, info, name=None):
       query = SkillObject.get_query(info=info)
       query = query.filter(
           SkillModel.profile_id == self.id)
       if name:
           query = query.filter(SkillModel.name == name)

       return query.all()

class SkillObject(SQLAlchemyObjectType):
   class Meta:
       model = SkillModel
       interface = (graphene.relay.Node, )


class SkillInput(graphene.InputObjectType):
   name = graphene.String()
   preferred_skill = graphene.Boolean()