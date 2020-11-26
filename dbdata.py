from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db',
                       connect_args={'check_same_thread': False})

Base = declarative_base()


class URLData(Base):
    __tablename__ = 'url_data'
    long_url = Column(String, unique=True)
    short_url = Column(String, unique=True)
    id = Column(Integer, primary_key=True)

    def __init__(self, long_url, short_url, host_url):
        self.long_url = long_url
        self.short_url = short_url
        self.host_url = host_url

    def get_short_url(self):
        url_data = URLData(long_url=self.long_url, short_url=self.short_url, host_url=self.host_url)
        session_global = sessionmaker(bind=engine)

        try:

            session = session_global()
            session.add(url_data)
            session.commit()

        except:

            # to handle uniqueness errors

            session = session_global()
            query = session.query(URLData)
            instance = query.filter_by(long_url=self.long_url).first()

            return instance.short_url

        return self.short_url

    def get_long_url(self):
        session_global = sessionmaker(bind=engine)
        session = session_global()
        
        try:

            query = session.query(URLData)
            instance = query.filter_by(short_url=self.short_url).first()
            return instance.long_url
        
        except:

            return self.host_url


Base.metadata.create_all(engine, checkfirst=True)
