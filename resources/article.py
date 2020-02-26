import datetime
import time
import uuid
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from models import db, ArticleSchema, Article, Subscription, Channel
from pprint import pprint

articles_schema = ArticleSchema(many=True)
article_schema = ArticleSchema()


class ArticleResource(Resource):
    """Article Manage"""

    @jwt_required
    def get(self):
        """Get articles the user has subscribed to
        @@@
        #### return
        ```
        {
        "data":[{
        "channel_title": "I code it",
            "updated": "2016-05-10T11:12:00",
            "channel_url": "http://icodeit.org/atom.xml",
            "title": "保护你的API（上）",
            "summary":"<h2>前后端分离之后</h2>\n\n<p>前后端分离之后，在部署上通过一个反向代理就可以...",
            "content":"<h2>保护你的API</h2>\n<p>在大部分时候，我们讨论API的设计时，会从功能的角度出发定义出完善的..."，
            "channel_title": "I code it",
             "url": "http://abruzzi.github.com/2016/05/about-session-and-security-api-1/",
             "channel_uuid": "8675ee43-d9eb-389b-b815-969f890c740d"
        },
        ]
        }
        ```
        @@@
        """
        current_user = get_jwt_identity()
        articles = db.session.query(Subscription.user_id,
                                    Article.content,
                                    Article.title, Article.summary, Article.channel_uuid, Article.channel_url,
                                    Article.channel_title,
                                    Article.updated, Article.url).filter(
            Subscription.user_id == current_user).filter(
            Subscription.channel_id == Article.channel_uuid).all()
        articles = articles_schema.dump(articles)

        pprint(articles)
        return {'status': 'success', 'data': articles}, 200

    def post(self):
        """Add article
        @@@
        #### args
        | args | nullable | type |
        |--------|--------|--------|
        |    url    |    false    |    str  |
        |    channel_url    |    false    |    str   |
        |    channel_title   |    false    |    str   |
        |    channel_uuid  |    false    |   str   |
        |    title  |    false    |   str   |
        |    content  |    false    |   str   |
        |    summary  |    false    |   str   |
        |    updated |    false    |   datetime  |
        @@@
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        json_data['inserttime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # json_data['updated'] = datetime.datetime.strptime(json_data['updated'], '%Y-%m-%dT%H:%M:%SZ').strftime(
        #     '%Y-%m-%d %H:%M:%S')
        #
        json_data['uuid'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, json_data['url']))
        article = Article(
            url=json_data['url'],
            uuid=json_data['uuid'],
            channel_url=json_data['channel_url'],
            channel_uuid=json_data['channel_uuid'],
            channel_title=json_data['channel_title'],
            title=json_data['title'],
            inserttime=json_data['inserttime'],
            content=json_data['content'],
            summary=json_data['summary'],
            updated=json_data['updated']
        )
        result = {}
        try:
            db.session.add(article)
            db.session.commit()
            result['status'] = 'success'
            result['data'] = json_data
            return jsonify(result)
        except Exception as e:
            result['status'] = 'failure'
            result['message'] = str(e)
            return jsonify(result)


class ChannelArticleResource(Resource):
    """Get articles for the specified channel source

    """

    def get(self, channel_id):
        """
        @@@
        #### return
        ```
        {
        "data":[{
        "channel_title": "I code it",
            "updated": "2016-05-10T11:12:00",
            "channel_url": "http://icodeit.org/atom.xml",
            "title": "保护你的API（上）",
            "summary":"<h2>前后端分离之后</h2>\n\n<p>前后端分离之后，在部署上通过一个反向代理就可以...",
            "content":"<h2>保护你的API</h2>\n<p>在大部分时候，我们讨论API的设计时，会从功能的角度出发定义出完善的...",
            "channel_title": "I code it",
             "url": "http://abruzzi.github.com/2016/05/about-session-and-security-api-1/",
             "channel_uuid": "8675ee43-d9eb-389b-b815-969f890c740d"

        },
        ]
        }
        ```
        @@@
        """
        articles = Article.query.filter_by(channel_uuid=channel_id).all()
        print(articles)
        articles = articles_schema.dump(articles)
        return {'status': 'success', 'data': articles}, 200

