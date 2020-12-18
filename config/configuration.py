import os


Base_Dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    SECRET_KEY = 'cc04e441377094a711d57563f358994ffd2b210148deb57450f4f40bdd085c6e'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    ITEMS_PER_PAGE = 20
    LANGUAGES = ['en', 'fr', 'es', 'por', 'ar']

    GEOIP_FILEPATH = os.path.join(Base_Dir, 'geo_lib\ip\GeoIP.dat')
    GEOIP_CACHE = 'STANDARD'
