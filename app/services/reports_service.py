from ..repositories.reports_repository import ReportsRepository


class ReportsService:

    @staticmethod
    def get_report_purchases():
        total_purchases = ReportsRepository.get_total_purchases()
        total_price = ReportsRepository.get_total_price()
        total_prices_by_genres_and_categories = ReportsRepository.get_total_prices_by_category_and_genre()
        most_sold_audio = ReportsRepository.get_most_sold_audios()

        # CALCULAR REVENUE
        
        return {
            "total_purchases": total_purchases, 
            "total_price": total_price,
            "total_price_by_category_and_genre": total_prices_by_genres_and_categories,
            "most_sold_audios": most_sold_audio
            }, 200
    
    @staticmethod
    def get_report_users():
        users_status_report = ReportsRepository.get_users_status_report()
        users_types_report = ReportsRepository.get_users_types_report()

        return {
            "users_by_status": users_status_report,
            "users_by_type": users_types_report
        }, 200
    
    @staticmethod
    def get_report_audios():
        total_audios = ReportsRepository.get_total_audios()
        most_favorited_audios = ReportsRepository.get_most_favorited_audios()
        total_by_category_and_genre = ReportsRepository.get_total_audios_by_category_and_genre()
        top_score_audios = ReportsRepository.get_top_rated_audios()

        return {
            "total_audios": total_audios,
            "most_favorited_audios": most_favorited_audios,
            "total_by_category_and_genre": total_by_category_and_genre,
            "top_score_audios": top_score_audios
        }, 200
    
    @staticmethod
    def get_report_creators():
        top_creators_by_points = ReportsRepository.get_top_creators_by_points()

        return {
            "top_creators_by_points": top_creators_by_points
        }, 200