from fastapi import FastAPI, Path, Response, status, HTTPException, Depends, APIRouter, File, UploadFile
from typing import Optional
from sqlalchemy.orm import Session
from .. import models, schemas
from .. database import get_db

from app.news_extraction import *
from app.analysts_ratings import *
from app.appRating import *
from app.insider_trades import *
from app.text_analysis import *
from app.financialStatementsAnalysis import *
from app.esg import *

router = APIRouter(
    tags=['Functionalities']
)

# GET METHOD for today's data
@router.get('/sentiment/{asset}', status_code=status.HTTP_202_ACCEPTED)
def sentiment_extraction(asset: str = Path(..., description = "Enter the asset name you want the sentiment analysis for: "), db: Session = Depends(get_db)): #current_user: int = Depends(oauth2.get_current_user)):
    try:
        #print(current_user.email)
        value = (news(asset))
        print(value)
        new_data = models.SentimentAnalysis(**value) #** unpacks the dictionary
        db.add(new_data)
        db.commit()
        db.refresh(new_data)

        return value
    except Exception as e:
        return {"error" : e}

@router.get('/summarize-financial-statements/{ticker}/{financial_statement}/{frequency}', status_code=status.HTTP_202_ACCEPTED)
def summarize_financial_statement(ticker: str = Path(..., description = "Enter the US company ticker name : "), financial_statement: str = Path(..., description = "Enter the financial statement you want a summary for (balance_sheet, cashflow or income_statement) : "), frequency: str = Path('quaterly', description = "Enter the frequency of the statements (quarterly or annual): "), db: Session = Depends(get_db)):
    try:
        #print(current_user.email)
        value = (analyse_financial_statements(ticker, financial_statement, frequency))
        print(value)
        #new_data = models.SummarizeFinancialStatement(**value)
        #db.add(new_data)
        #db.commit()
        #db.refresh(new_data)

        return value
    except Exception as e:
        return {"error" : e}

@router.get('/playstore-reviews-analysis/{company}', status_code=status.HTTP_202_ACCEPTED)
def google_playstore_app_reviews(company: str = Path(..., description = "Enter the company you want Google Playstore Review Analysis for: ")): # , db: Session = Depends(get_db)):
    try:
        review_analysis = (get_google_playstore_app_reviews(company))
        print(review_analysis)
        #connecting database
        #new_data = models.GooglePlayStoreReviewAnalysis(**review_analysis) #** unpacks the dictionary
        #db.add(new_data)
        #db.commit()
        #db.refresh(new_data)

        return review_analysis
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

@router.get('/esg/{US_stock_ticker}' ,status_code=status.HTTP_202_ACCEPTED)
def esg(US_stock_ticker: str = Path(..., description = "Enter the TICKER of the company: ")): # Not using DataBase because response can differ
    try:
        esg_df = esg_scores(US_stock_ticker)
        return esg_df
    except:
        return {"Error" : "Are you sure you've entered a US Stock Ticker? Maybe try again?"}

@router.get('/analyst-ratings/{US_stock_ticker}' ,status_code=status.HTTP_202_ACCEPTED)
def analyst_ratings(US_stock_ticker: str = Path(..., description = "Enter the TICKER of the company: ")): # Not using DataBase because response can differ
    try:
        rating = analyst_rating(US_stock_ticker)

        return rating
    except:
        return {"Error" : "Are you sure you've entered a US Stock Ticker? Maybe try again?"}

@router.get('/insider-trades/{US_stock_ticker}' ,status_code=status.HTTP_202_ACCEPTED)
def insider_trades(US_stock_ticker: str = Path(..., description = "Enter the TICKER of the company: "), db: Session = Depends(get_db)):
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