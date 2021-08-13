from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

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


def abort_video_exists(video_id):
    # get video id
    video = videos.get(video_id)
    # send error message if video exists
    if video:
        abort(409, ErrorMessage="Video already exists!")


def abort_video_doesnt_exists(video_id):
    # get video id
    video = videos.get(video_id)
    # send error message if video doesn't exists
    if not video:
        abort(404, ErrorMessage="Video ID is not valid!")

    return video


class Base(Resource):
    def get(self):
        return {
            "video": "/video",
        }


class Video(Resource):
    def get(self, video_id):
        # validate video id
        video = abort_video_doesnt_exists(video_id)

        return video, 200

    def put(self, video_id):
        # validate video id
        abort_video_exists(video_id)

        # validate and add video info
        args = video_out_args.parse_args()
        videos[video_id] = args

        return {video_id: args}, 201

    def delete(self, video_id):
        # validate video id
        video = abort_video_doesnt_exists(video_id)

        if video:
            del videos[video_id]

        return 200

api.add_resource(Base, "/")
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
