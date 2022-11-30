from fastapi import FastAPI, Path, Response, status, HTTPException, Depends, APIRouter, File, UploadFile
from typing import Optional
from sqlalchemy.orm import Session
from .. import models, schemas
from .. database import get_db

from app.news_extraction import *
from app.short_interest import *
from app.analysts_ratings import *
from app.insider_trades import *
from app.text_analysis import *

router = APIRouter(
    tags=['Functionalities']
)

# GET METHOD for today's data
@router.get('/sentiment/{asset}', status_code=status.HTTP_202_ACCEPTED)
def sentiment_extraction(asset: str = Path(None, description = "Enter the asset name you want the sentiment analysis for: "), db: Session = Depends(get_db)): #current_user: int = Depends(oauth2.get_current_user)):
    try:
        #print(current_user.email)
        value = (news(asset))
        new_data = models.SentimentAnalysis(**value) #** unpacks the dictionary
        db.add(new_data)
        db.commit()
        db.refresh(new_data)

        return value
    except Exception as e:
        return {"error" : e}
    
@router.post('/text-analysis/' ,status_code=status.HTTP_202_ACCEPTED)
async def text_file_analysis(file: UploadFile = File(...)):
    try:
        response = await file.read()
        
        analysis = text_analysis(response)

        return analysis
    except Exception as e:
        return {"Error" : e}
        #return {"Error" : "Are you sure you've provided a Text (.txt) Document?"}

@router.get('/short-interest/{asset}', status_code=status.HTTP_202_ACCEPTED)
def short_interest(asset: str = Path(None, description = "Enter the TICKER of the company: "), db: Session = Depends(get_db)): #, user_id: int = Depends(oauth2.get_current_user)):
    try:
        short_interest_value = short_info(asset)
        new_data = models.ShortInterest(**short_interest_value) #** unpacks the dictionary
        db.add(new_data)
        db.commit()
        db.refresh(new_data)

        return short_interest_value
    except:
        return {"error" : "There is no short interest data available on {} yet. Have you entered a valid ticker? If yes, then kindly check back later".format(asset)}

@router.get('/analyst-ratings/{US_stock_ticker}' ,status_code=status.HTTP_202_ACCEPTED)
def analyst_ratings(US_stock_ticker: str = Path(None, description = "Enter the TICKER of the company: ")): # Not using DataBase because response can differ
    try:
        rating = analyst_rating(US_stock_ticker)

        return rating
    except:
        return {"Error" : "Are you sure you've entered a US Stock Ticker? Maybe try again?"}

@router.get('/insider-trades/{US_stock_ticker}' ,status_code=status.HTTP_202_ACCEPTED)
def insider_trades(US_stock_ticker: str = Path(None, description = "Enter the TICKER of the company: "), db: Session = Depends(get_db)):
    try:
        insider_trades = insider_trades_data(US_stock_ticker)

        for new_data in insider_trades:
            data = models.InsiderTrades(**new_data)

            print(data)
            db.add(data)
            db.commit()
            db.refresh(data)

        return insider_trades
    except Exception as e:
        print(e)
        return {"Error" : "Are you sure you've entered a US Stock Ticker? Maybe try again?"}