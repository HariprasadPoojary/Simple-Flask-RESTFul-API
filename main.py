from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

# * Models
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Video: {self.name}"


#! Only Run below code the first you create your Models, this creates database tables
# db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name",
    type=str,
    required=True,
    help="Required: Name of the video",
)
video_put_args.add_argument(
    "likes",
    type=int,
    required=True,
    help="Required: Likes on the video",
)
video_put_args.add_argument(
    "views",
    type=int,
    required=True,
    help="Required: Views of the video",
)

video_patch_args = reqparse.RequestParser()
video_patch_args.add_argument(
    "name",
    type=str,
)
video_patch_args.add_argument(
    "likes",
    type=int,
)
video_patch_args.add_argument(
    "views",
    type=int,
)

# * serializer result object
resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer,
}

# * Views
class Base(Resource):
    def get(self):
        return {
            "video": "/video",
        }


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        # get video id or abort with 404
        video = VideoModel.query.filter_by(id=video_id).first_or_404(
            description="Video ID does not exists!"
        )

        return video, 200

    @marshal_with(resource_fields)
    def put(self, video_id):
        # validate and get argumets received
        args = video_put_args.parse_args()
        # check if video exists
        db_video = VideoModel.query.filter_by(id=video_id).first()

        if not db_video:
            # create new Model instance
            video = VideoModel(
                id=video_id,
                name=args["name"],
                views=args["views"],
                likes=args["likes"],
            )
            # add this instance to database
            db.session.add(video)
            # commit to database
            db.session.commit()
            # this return object will be serialized by marshal_with decorator
            return video, 201

        abort(409, ErrorMessage="VideoID already exists!")

    @marshal_with(resource_fields)
    def patch(self, video_id):
        # check if video exists
        db_video = VideoModel.query.filter_by(id=video_id).first()
        if not db_video:
            abort(406, ErrorMessage="VideoID already exists!")

        # validate and get argumets received
        args = video_patch_args.parse_args()

        # update model parameters based on individual parameters
        if args["name"]:
            db_video.name = args["name"]
        if args["views"]:
            db_video.views = args["views"]
        if args["likes"]:
            db_video.likes = args["likes"]
        # commit
        db.session.commit()

        return db_video, 202

    def delete(self, video_id):
        # validate video id
        video = VideoModel.query.filter_by(id=video_id).first_or_404(
            description="Video ID does not exists!"
        )
        # delete the video
        db.session.delete(video)
        # commit
        db.session.commit()

        return 200


# * Routing
api.add_resource(Base, "/")
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
