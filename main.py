from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

video_out_args = reqparse.RequestParser()
video_out_args.add_argument(
    "name",
    type=str,
    required=True,
    help="Required: Name of the video",
)
video_out_args.add_argument(
    "likes",
    type=int,
    required=True,
    help="Required: Likes on the video",
)
video_out_args.add_argument(
    "views",
    type=int,
    required=True,
    help="Required: Views of the video",
)

videos = {}


class Base(Resource):
    def get(self):
        return {
            "video": "/video",
        }


class Video(Resource):
    def get(self, video_id):
        return videos[video_id]

    def put(self, video_id):
        args = video_out_args.parse_args()
        videos[video_id] = args
        return {video_id: args}, 201


api.add_resource(Base, "/")
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
