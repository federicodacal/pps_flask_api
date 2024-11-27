import os

class ConfigService:
    API_URL = {
        'dev': 'http://localhost:5000',
        'prod': 'https://pps-flask-api.vercel.app'
    }
    current_url = API_URL['dev']

    @classmethod
    def set_environment(cls, environment):
        cls.current_url = cls.API_URL.get(environment, cls.API_URL['dev'])