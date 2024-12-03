import datetime

from sqlalchemy import desc, func

from ..models.user_detail import User_detail
from ..models.favorites import Favorite
from ..models.audio import Audio
from ..models.purchase import Purchase
from ..models.creator import Creator
from ..models.user import User
from ..models.purchase_detail import Purchase_detail
from ..models.item import Item
from ..databases.db import db
from sqlalchemy.orm import joinedload

class ReportsRepository:

    @staticmethod
    def get_total_purchases():
        return db.session.query(func.count(Purchase_detail.ID)).scalar() #type: ignore
    
    @staticmethod
    def get_total_price():
        return db.session.query(func.sum(Item.price)).join(Purchase_detail, Purchase_detail.item_ID == Item.ID).scalar() #type: ignore
    
    @staticmethod
    def get_total_prices_by_category_and_genre():
        # Total por categoría
        category_totals = (
            db.session.query(
                Audio.category.label('category'), # type: ignore
                func.sum(Item.price).label('total_price') #type: ignore
            )
            .join(Item, Item.audio_ID == Audio.ID) # type: ignore
            .join(Purchase_detail, Purchase_detail.item_ID == Item.ID) #type: ignore
            .filter(Purchase_detail.state == 'created') #type: ignore
            .group_by(Audio.category) #type: ignore
            .all()
        )

        # Total por género
        genre_totals = (
            db.session.query(
                Audio.genre.label('genre'), #type: ignore
                func.sum(Item.price).label('total_price') #type: ignore
            )
            .join(Item, Item.audio_ID == Audio.ID) #type: ignore
            .join(Purchase_detail, Purchase_detail.item_ID == Item.ID) #type: ignore
            .filter(Purchase_detail.state == 'created') #type: ignore
            .group_by(Audio.genre) #type: ignore
            .all()
        )

        return {
            "by_category": [{"category": row.category, "total_price": row.total_price} for row in category_totals],
            "by_genre": [{"genre": row.genre, "total_price": row.total_price} for row in genre_totals]
        }
    
    @staticmethod 
    def get_most_sold_audios():
        most_sold_audios = (
            db.session.query(
                Audio.ID.label('audio_id'), Audio.audio_name, func.count(Purchase_detail.ID).label('total_sales')) #type: ignore
            .join(Item, Item.audio_ID == Audio.ID) #type: ignore
            .join(Purchase_detail, Purchase_detail.item_ID == Item.ID) #type: ignore
            .filter(Purchase_detail.state == 'created') #type: ignore
            .group_by(Audio.ID, Audio.audio_name) #type: ignore
            .order_by(desc(func.count(Purchase_detail.ID))) #type: ignore
            .limit(3)
            .all()
        )

        if most_sold_audios:
            result = [
                {
                    "audio_id": audio.audio_id,
                    "audio_name": audio.audio_name,
                    "total_sales": audio.total_sales
                }
                for audio in most_sold_audios
            ]

        return result
    
    @staticmethod 
    def get_users_status_report():
        total_users = db.session.query(func.count(User.ID)).scalar() #type: ignore
        created_users = db.session.query(func.count(User.ID)).filter(User.state == 'created').scalar() #type: ignore
        active_users = db.session.query(func.count(User.ID)).filter(User.state == 'active').scalar() #type: ignore
        inactive_users = db.session.query(func.count(User.ID)).filter(User.state == 'inactive').scalar() #type: ignore

        return {
            "total_users" : total_users,
            "created_users" : created_users,
            "active_users" : active_users,
            "inactive_users" : inactive_users
        }


    @staticmethod 
    def get_users_types_report():
        creators = db.session.query(func.count(User.ID)).filter(User.type == 'creator').scalar() #type: ignore
        buyers = db.session.query(func.count(User.ID)).filter(User.type == 'buyer').scalar() #type: ignore
        mods = db.session.query(func.count(User.ID)).filter(User.type == 'mod').scalar() #type: ignore

        return {
            "creators" : creators,
            "buyers" : buyers,
            "mods" : mods
        }
    
    @staticmethod
    def get_total_audios():
        return db.session.query(func.count(Audio.ID)).scalar() #type: ignore
    
    @staticmethod
    def get_most_favorited_audios():
        most_favorited_audios = db.session.query( 
        Audio.audio_name, func.count(Favorite.ID).label("favorites_count")).join(Favorite, Favorite.audio_ID == Audio.ID).group_by(Audio.ID).order_by(desc("favorites_count")).limit(5).all() #type: ignore

        result = [
        {"audio_name": row.audio_name, "favorites_count": row.favorites_count}
        for row in most_favorited_audios
        ]
        return result
    
    @staticmethod
    def get_total_audios_by_category_and_genre():
        total_by_genre = db.session.query(
            Audio.genre, func.count(Audio.ID).label("total_count")).group_by(Audio.genre).all() #type: ignore

        total_by_category = db.session.query(
            Audio.category, func.count(Audio.ID).label("total_count")).group_by(Audio.category).all() #type: ignore
        
        serialized_genre = [
        {"genre": row.genre, "total_count": row.total_count}
        for row in total_by_genre
        ]
        serialized_category = [
            {"category": row.category, "total_count": row.total_count}
            for row in total_by_category
        ]

        return {
            "total_by_genre": serialized_genre,
            "total_by_category": serialized_category
        }
    
    @staticmethod
    def get_top_rated_audios():
        top_rated_audios = db.session.query(
            Audio.audio_name, Audio.score).order_by(desc(Audio.score)).limit(5).all()  # type: ignore

        result = [
            {"audio_name": row.audio_name, "score": row.score}
            for row in top_rated_audios
        ]
        return  result
    
    @staticmethod
    def get_top_creators_by_points():
        top_creators_by_points = db.session.query(Creator.ID, User_detail.username, User_detail.full_name, Creator.points).join(User, User.ID == Creator.user_ID).join(User_detail, User.user_detail_ID == User_detail.ID).order_by(desc(Creator.points)).limit(5).all() #type: ignore

        result = [
            {"creator": row.ID, "points": row.points}
            for row in top_creators_by_points
        ]
        return  result
    