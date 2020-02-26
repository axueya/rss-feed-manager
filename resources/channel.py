import datetime
import uuid

from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models import db, ChannelSchema, Channel

channels_schema = ChannelSchema(many=True)
channel_schema = ChannelSchema()


class ChannelResource(Resource):
    """RSS Channel Source Manage"""

    # @jwt_required
    def get(self):
        """Get all rss channels

        @@@
        #### example
        ```
        {
        "data": [
            {
            "tags": "技术博客",
            "inserttime": "2020-01-18T17:19:45",
            "url": "http://www.raychase.net/channel",
            "categories": "技术博客",
            "title": "四火的唠叨",
            "uuid": "041ef560-d670-3316-a772-45b2b3e70020"
            }
           ]
        }
        ```
        @@@
        """

        channels = Channel.query.all()
        channels = channels_schema.dump(channels)
        print(channels)
        return {'data': channels}

    def post(self):
        """ Add rss channels
        @@@
        #### args

        | args | nullable | type |
        |--------|--------|--------|
        |    url    |    false    |    str  |
        |    categories    |    false    |    str   |
        |    tags   |    false    |    str   |
        |    title  |    false    |   str   |


        #### example
        ```
        input:
        {
          "categories": "技术博客",
          "tags":"技术博客",
          "title": "I code it",
          "url": "http://icodeit.org/atom.xml"

        }
        output:
        {
          "status": "success",
          "data": {
            "categories": "技术博客",
            "tags": "技术博客",
            "title": "I code it",
            "url": "http://icodeit.org/atom.xml",
            "inserttime": "2020-01-18 19:17:43",
            "uuid": "8675ee43-d9eb-389b-b815-969f890c740d"
          }
        }
        ```
        @@@

        """
        json_data = request.get_json(force=True)
        print(json_data)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        json_data['inserttime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        json_data['uuid'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, json_data['url']))
        print(json_data)

        channel = Channel(
            url=json_data['url'],
            categories=json_data['categories'],
            tags=json_data['tags'],
            title=json_data['title'],
            inserttime=json_data['inserttime'],
            uuid=json_data['uuid']

        )
        result = {}
        try:
            db.session.add(channel)
            db.session.commit()
            result['status'] = 'success'
            result['data'] = json_data
            return jsonify(result)
        except Exception as e:
            result['status'] = 'failure'
            result['message'] = str(e)
            return jsonify(result)


class ChannelItemResource(Resource):

    def get(self, id):
        channel = Channel.query.filter_by(id=id)
        channel = channels_schema.dump(channel)
        return {'status': 'success', 'data': channel}, 200

