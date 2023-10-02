from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary

db = SQLAlchemy()

class SavedVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    video_file = db.Column(LargeBinary())
    transcript = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    video_url = db.Column(db.String(255), nullable=False)

    # Function to save a video to the SavedVideo table
    @staticmethod
    def save_video_to_database(name: str, video_file: bytes, video_url: str, transcript: str = None) -> bool:
        try:
            with db.session() as session:
                new_video = SavedVideo(name=name, video_file=video_file, video_url=video_url, transcript=transcript)
                session.add(new_video)
                session.commit()
            return True
        except Exception as e:
            print(f"Error saving video to the database: {str(e)}")
            return False
