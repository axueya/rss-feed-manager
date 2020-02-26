from models import UserSchema
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from models import User
from blacklist import BLACKLIST

users_schema = UserSchema(many=True)
user_schema = UserSchema()

_parser = reqparse.RequestParser()
_parser.add_argument('username',
                     type=str,
                     required=True,
                     help="This field cannot be blank."
                     )
_parser.add_argument('password',
                     type=str,
                     required=True,
                     help="This field cannot be blank."
                     )


class UserRegister(Resource):

    def post(self):
        """User Register
        @@@

        #### input
        ```
        {
        "username":"test",
        "password":"test"
        }
        ```
        #### output
        ```
        {
            "message": "User created successfully."
        }
        ```
        @@@
        """
        data = _parser.parse_args()
        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        data['password'] = generate_password_hash(data['password'])
        user = User(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserResource(Resource):
    @classmethod
    def get(cls, user_id):
        """Get User by Id
        @@@

        #### input
        ```
        /api/v1.0/users/1
        ```

        #### output:
        ```
        {
            "id": 1,
            "username": "test"
        }
        ```
        @@@
        """
        user = User.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    # @classmethod
    # def delete(cls, user_id):
    #     """Delete user by Id
    #
    #     """
    #     user = User.find_by_id(user_id)
    #     if not user:
    #         return {'message': 'User not found'}, 404
    #     user.delete_from_db()
    #     return {'message': 'User deleted'}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        """Login and return access_token and refresh_token
        @@@

        #### input
        ```

        {
        "username":"test",
        "password":"test"
        }
        ```

        #### output:
        ```
        {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Nzk0OTQzNTgsIm5iZiI6MTU3OTQ5NDM1OCwianRpIjoiNzk5OTFjMjQtNjdlYS00ZmEyLWEyY2ItMWE3NDEwNGU5ZmJhIiwiZXhwIjoxNTc5NTgwNzU4LCJpZGVudGl0eSI6MSwiZnJlc2giOnRydWUsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJpc19hZG1pbiI6dHJ1ZX19.lWuI0X5z61w4MllW_A-JCaJet1yKN2VB_sQiHGOPGXI",
            "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Nzk0OTQzNTgsIm5iZiI6MTU3OTQ5NDM1OCwianRpIjoiNjI2YjI4NjktZWY0OC00MGRkLTkzNzMtZmUxZTMyMGE4ZmJhIiwiZXhwIjoxNTgyMDg2MzU4LCJpZGVudGl0eSI6MSwidHlwZSI6InJlZnJlc2gifQ.wIv_pXuDTpybfHTVfezfk8AYDnbmxMQc14pKr3jE7Us"
        }
        ```
        @@@
        """

        # get data from parser
        data = _parser.parse_args()
        # find user in database
        user = User.find_by_username(data['username'])
        # check password

        if user and check_password_hash(user.password, data['password']):
            # create access token
            access_token = create_access_token(identity=user.id, fresh=True)
            # create refresh token
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        # return them
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        """Logout and expired token
        @@@

        #### input(Add Authorization to header)
        ```
        {
        "username":"test",
        "password":"test"
        }

        ```

        #### output:
        ```
        {
            "message": "Successfully logged out"
        }
        ```
        @@@
        """
        jti = get_raw_jwt()['jti']  # jti stands fro 'JWT ID' a unique identifier for a JWT
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out'}, 200


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        """Refresh token if it is expired
        @@@
        Add Authorization to header. value=Bearer refresh token
        #### output
        ```
        {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Nzk0OTUwNzIsIm5iZiI6MTU3OTQ5NTA3MiwianRpIjoiYWU2ODY1NTEtNDFkNC00OWZmLTgwZmUtNDJhOGMyODY2ZmIxIiwiZXhwIjoxNTc5NTgxNDcyLCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIiwidXNlcl9jbGFpbXMiOnsiaXNfYWRtaW4iOnRydWV9fQ.pa7bPBtofmv_2fGtDMlu6BC1sDA24tXkSxt2byFHPmM"
        }
        ```
        @@@
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200

