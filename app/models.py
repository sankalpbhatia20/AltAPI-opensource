# TO STORE MODELS OF OUR DATABASE TABLES
from .database import Base
from sqlalchemy import Column, Integer, Text, Date, Numeric, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.dialects.postgresql import UUID
import uuid

class SentimentAnalysis(Base):
    __tablename__ = 'sentiment_today' # Table name

    id = Column(String, primary_key = True, nullable = False)
    asset = Column(String, nullable = False)
    date = Column(Date, nullable = False)
    compound_positivity_score = Column(Numeric, nullable = False)
    compound_sentiment = Column(String, nullable = False)
    top_url = Column(Text, nullable = False)
    top_url_summary = Column(Text, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class ShortInterest(Base):
    __tablename__ = 'short_interest' # Another table name

    id = Column(String, primary_key = True, nullable = False)
    asset = Column(String, nullable = False)
    date = Column(Date, nullable = False)
    short_interest = Column(String, nullable = True)
    short_interest_percentage = Column(String, nullable = True)
    days_to_cover = Column(Integer, nullable = True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class InsiderTrades(Base):
    __tablename__ = 'insider_trades'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    index = Column(Integer, nullable = False)
    asset = Column(String, nullable = False)
    date = Column(String, nullable = False)
    position = Column(String, nullable = False)
    transaction = Column(String, nullable = False)
    number_of_shares = Column(String, nullable = False)
    cost = Column(Numeric, nullable = False)
    value = Column(String, nullable = False)
    total_number_of_shares = Column(String, nullable = False)
    insider_trader = Column(String, nullable = False)
    SEC_form_4 = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))