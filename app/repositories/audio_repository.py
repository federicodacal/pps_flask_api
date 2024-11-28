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
        return (Audio.query.options(joinedload(Audio.item)).all()) # type: ignore
    
    @staticmethod
    def get_audio_by_id_with_item(audio_id):
        return Audio.query.options(joinedload(Audio.item)).filter_by(ID=audio_id).first() # type: ignore
    
    @staticmethod
    def get_audios_by_creator(creator_id):
        return Audio.query.options(joinedload(Audio.item)).filter_by(creator_ID=creator_id).all() #type: ignore

    @staticmethod
    def create_audio(data, file_id):
        new_audio = Audio(
            creator_ID=data['creator_ID'],
            file_name=file_id,
            audio_name=data['audio_name'],
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
    
    @staticmethod
    def update_audio(ID, data):
        audio = Audio.query.get(ID)

        if not audio:
            return None

        audio.audio_name = data.get('audio_name', audio.audio_name)
        audio.state = data.get('state', audio.state)
        audio.category = data.get('category', audio.category)
        audio.genre = data.get('genre', audio.genre)
        audio.BPM = data.get('BPM', audio.BPM)
        audio.tone = data.get('tone', audio.tone)
        audio.length = data.get('length', audio.length)
        audio.size = data.get('size', audio.size)
        audio.modified_at = datetime.datetime.now(datetime.timezone.utc)
        
        return audio
    
    @staticmethod
    def delete_audio(audio_id):
        audio = Audio.query.get(audio_id)
        if audio:
            db.session.delete(audio)

    @staticmethod
    def update_state_audio(ID, state):
        audio = Audio.query.get(ID)

        if not audio: 
            return None
        
        audio.state = state
        audio.modified_at = datetime.datetime.now(datetime.timezone.utc) 

        return audio
    
    @staticmethod
    def add_points_to_audio(ID, points):
        audio = Audio.query.get(ID)
        if not audio:
            return None
        
        audio.score += points
        audio.modified_at = datetime.datetime.now(datetime.timezone.utc)
       
        return audio
