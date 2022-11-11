# Custom decorators
from functools import wraps
import requests
import os
from include.models import Stocks_Owned


def logout_required(current_user, redirect):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # If user is already logged in redirect to home page.
            if current_user.is_authenticated:
                return redirect('/')
            return func(*args, **kwargs)
        return wrapper
    return decorate


def login_required(current_user, redirect):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # If user is not logged in redirect to home page.
            if not current_user.is_authenticated:
                return redirect('/')
            return func(*args, **kwargs)
        return wrapper
    return decorate


def lookup_symbol(symbol):
    # Request the api for information.
    try:
        token = os.environ['IEX']
        #token = 'Tpk_c1f51c49da9c413a9ea676bfd7322915'
        url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=logo,company,quote,news&token={token}'
        #url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=Logo,company,quote&token={token}'
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None
    
    # Return the response in JSON format.
    return response.json()


def lookup_symbol_quote(symbol):
    # Request the api for information.
    try:
        token = os.environ['IEX']
        #token = 'Tpk_c1f51c49da9c413a9ea676bfd7322915'
        url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote&token={token}'
        #url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=Logo,company,quote&token={token}'
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None
    
    # Return the response in JSON format.
    return response.json()


def update_price(current_user, session):
    # Update the price of every stock owned by the current user and add it in the session variable.
    stocks = Stocks_Owned.query.filter_by(user_id = current_user.id).all()
    for stock in stocks:
        if stock not in session:
            data = lookup_symbol(stock.stock_id)
            session[stock.stock_id] = data
        else: 
            quote = lookup_symbol_quote(stock.stock_id)
            session[stock.stock_id][stock.stock_id]['quote'] = quote
    