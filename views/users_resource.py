from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from sqlalchemy import select

from data import db_session
from data.user_request_parser import user_parser
from data.users import User

app = Flask(__name__)
api = Api(app)


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(User).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        news = session.query(User).get(user_id)
        return jsonify({'news': news.to_dict(
            only=('title', 'content', 'user_id', 'is_private'))})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        result = db_sess.execute(
            select(User)
        )
        users = result.all()
        fields = ('name', 'surname', 'age', 'address', 'email',
                  'position', 'speciality')
        users_dict = [user.to_dict(only=fields) for user, in users]
        return jsonify({
            'jobs': users_dict,
        })

    def post(self):
        args = user_parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            address=args['address'],
            email=args['email'],
            position=args['position'],
            speciality=args['speciality'],
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
