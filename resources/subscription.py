import datetime

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from models import Subscription, Channel, db, UserSubscriptionSchema

subscriptions_schema = UserSubscriptionSchema(many=True)
subscription_schema = UserSubscriptionSchema()


class SubscriptionResource(Resource):
    """Subscription Manage"""

    @jwt_required
    def get(self):
        """Get all subscriptions
        @@@
        #### return
        ```
        {
            "data": [
                {
                    "url": "http://www.raychase.net/channel",
                    "user_id": 1,
                    "categories": "技术博客",
                    "channel_id": "041ef560-d670-3316-a772-45b2b3e70020",
                    "inserttime": "2020-01-19T11:16:59",
                    "title": "四火的唠叨",
                    "tags": "技术博客"
                }
            ]
        }
        ```
        @@@
        """
        current_user = get_jwt_identity()

        subscriptions = db.session.query(Subscription.user_id, Subscription.channel_id,
                                         Subscription.inserttime,
                                         Channel.title, Channel.tags, Channel.categories, Channel.url).filter(
            Subscription.user_id == current_user).filter(
            Subscription.channel_id == Channel.uuid).all()

        subscriptions = subscriptions_schema.dump(subscriptions)

        print(subscriptions)
        return {'data': subscriptions}

    @jwt_required
    def post(self):
        """Add/Delete subscription
        @@@
         #### args

        | args | nullable | type |
        |--------|--------|--------|
        |    user_id    |    false    |    str  |
        |    op    |    false    |    str   |
        #### input

        ```
            {
            "channel_id":"041ef560-d670-3316-a772-45b2b3e70020",
            "op":"insert"
            }
        ```

        #### output
        ```
        {
          "status": "success",
          "data": {
            "user_id": 1,
            "channel_id": "041ef560-d670-3316-a772-45b2b3e70020",
            "inserttime": "2020-01-19 11:16:59"
          }
        }
        ```
        @@@
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        json_data['inserttime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(json_data)
        current_user = get_jwt_identity()
        json_data['user_id'] = current_user
        result = {}

        if json_data['op'] == 'insert':
            if isinstance(json_data['channel_id'], str):
                subscription = Subscription(
                    user_id=json_data['user_id'],
                    channel_id=json_data['channel_id'],
                    inserttime=json_data['inserttime']
                )
                try:
                    db.session.add(subscription)
                    db.session.commit()
                    result['status'] = 'success'
                    result['data'] = json_data
                    return jsonify(result)
                except Exception as e:
                    result['status'] = 'failure'
                    result['message'] = str(e)
                    return jsonify(result)
            elif isinstance(json_data['channel_id'], list):
                subscriptions = [Subscription(
                    user_id=json_data['user_id'],
                    channel_id=item,
                    inserttime=json_data['inserttime']
                ) for item in json_data['channel_id']]
                try:
                    db.session.add_all(subscriptions)
                    db.session.commit()
                    result['status'] = 'success'
                    result['data'] = json_data
                    return jsonify(result)
                except Exception as e:
                    result['status'] = 'failure'
                    result['message'] = str(e)
                    return jsonify(result)
        elif json_data['op'] == 'delete':
            if isinstance(json_data['channel_id'], str):
                obj = db.session.query(Subscription).filter(Subscription.channel_id == json_data['channel_id']).filter(
                    Subscription.user_id == current_user).one()
                try:
                    db.session.delete(obj)
                    db.session.commit()
                    result['status'] = 'success'
                    return jsonify(result)
                except Exception as e:
                    result['status'] = 'failure'
                    result['message'] = str(e)
                    return jsonify(result)
            elif isinstance(json_data['channel_id'], list):
                db.session.query(Subscription).filter(Subscription.channel_id.in_(json_data['channel_id'])).filter(
                    Subscription.user_id == current_user).delete(synchronize_session=False)
                try:
                    db.session.commit()
                    result['status'] = 'success'
                    return jsonify(result)

                except Exception as e:
                    result['status'] = 'failure'
                    result['message'] = str(e)
                    return jsonify(result)
        else:
            result['status'] = 'failure'
            result['message'] = 'op field should not be insert/delete'
            return jsonify(result)
