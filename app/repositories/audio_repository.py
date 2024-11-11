import datetime
from ..databases.db import db
from ..models.audio import Audio
from sqlalchemy.orm import joinedload

class AudioRepository:

    @staticmethod
    def get_all_audios():
        return Audio.query.all()
    
    @staticmethod
    def get_all_audios_with_items():
        return Audio.query.options(joinedload(Audio.item)).all() # type: ignore
    
    @staticmethod
    def get_audio_by_id_with_item(audio_id):
        return Audio.query.options(joinedload(Audio.item)).filter_by(ID=audio_id).first() # type: ignore
    
    @staticmethod
    def create_audio(data, file_id):
        new_audio = Audio(
            ID=data['ID'],
            creator_ID=data['creator_ID'],
            file_name=file_id,
            audio_name=data['audio_name'],
            state=data['state'],
            category=data['category'],
            genre=data['genre'],
            BPM=data['BPM'],
            tone=data['tone'],
            length=data['length'],
            size=data['size'],
            description=data['description'],
            created_at=datetime.datetime.now(datetime.timezone.utc),
            modified_at=datetime.datetime.now(datetime.timezone.utc)
        )
        db.session.add(new_audio)
        return new_audio