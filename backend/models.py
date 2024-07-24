from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Trader(Base):
    __tablename__ = 'traders'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    win_rate = Column(Float, nullable=False)
    trades = relationship('Trade', back_populates='trader')


class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)
    trader_id = Column(Integer, ForeignKey('traders.id'))
    conviction_level = Column(Float, nullable=False)
    trader = relationship('Trader', back_populates='trades')


class Leaderboard(Base):
    __tablename__ = 'leaderboard'
    id = Column(Integer, primary_key=True)
    trader_id = Column(Integer, ForeignKey('traders.id'))
    rank = Column(Integer, nullable=False)
    trader = relationship('Trader')


class Staking(Base):
    __tablename__ = 'staking'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    amount_staked = Column(Float, nullable=False)
    reward = Column(Float, nullable=False)


# Database setup
engine = create_engine('sqlite:///trading_platform.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
