from flask import Blueprint
from flask_restful import Api

from resources.article import ArticleResource, ChannelArticleResource
from resources.channel import ChannelResource, ChannelItemResource
from resources.subscription import SubscriptionResource
from resources.user import UserResource, UserLogin, UserLogout, TokenRefresh, UserRegister

api_bp = Blueprint('api/v1.0', __name__)
api = Api(api_bp)

api.add_resource(ChannelResource, '/channels')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(ChannelItemResource, '/channels/<int:id>')
api.add_resource(SubscriptionResource, '/subscriptions')
api.add_resource(ArticleResource, '/articles')
api.add_resource(ChannelArticleResource, '/articles/channels/<string:channel_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserRegister, '/register')
