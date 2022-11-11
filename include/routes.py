from flask import Flask, render_template, url_for, flash, redirect, jsonify, request, session
from include.forms import LoginForm, RegistrationForm, PurchaseForm, SellForm
from include.models import User, Stock, Stocks_Owned, Transaction
from include import app, db
from flask_login import login_user, current_user, logout_user
from include.utils import logout_required, login_required, lookup_symbol, lookup_symbol_quote, update_price
from datetime import datetime
import yfinance
import plotly.graph_objects as go
import plotly.offline as pyo
import json
from include.predictor import predict

@app.route('/')
@app.route('/home')
def index():
    #if current_user:
    #   update_price(current_user, session)
    return render_template('about.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods = ['GET', 'POST'])
@logout_required(current_user, redirect)
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Create a new instance of the user.
        user = User(username = form.username.data, email = form.email.data, password = form.password.data)

        # Add the user to the database.
        db.session.add(user)
        db.session.commit()

        # SQL equivalent:
        # INSERT INTO user (username, email, password) VALUES (form.username, form.email, password_hash)
        
        # Let the user know that the account has been created.
        flash(f'Account successfully created for {form.username.data}', category = 'success')
        
        # Redirect to the login page.
        return redirect(url_for('login'))

    elif form.errors != {}:
        for category, err_msgs in form.errors.items():
            for err_msg in err_msgs:
                flash(f'There was an error creating user: {err_msg}', category = 'danger')

    return render_template('register.html', form = form)


@app.route('/login', methods = ['GET', 'POST'])
@logout_required(current_user, redirect)
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Find a user with the given credentials
        user = User.query.filter_by(email = form.email.data).first()

        # If credentials are correct, than log in the user.
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful.', category = 'success')
            #update_price(current_user, session)
            return redirect(url_for('quote'))
        else: 
            flash('Login unsuccessful. Please check email and password.', category = 'danger')
    return render_template('login.html', form = form)


@app.route('/logout')
@login_required(current_user, redirect)
def logout():
    logout_user()
    flash('You were logged out of your account.', category = 'primary')
    return redirect(url_for('index'))


@app.route('/availableStocks')
@login_required(current_user, redirect)
def available_stocks():
    return render_template('available_stocks.html')


@app.route('/quote', methods = ['GET', 'POST'])
@login_required(current_user, redirect)
def quote():
    # Default views for users.
    views = ['Overview', 'Fundamentals', 'News']
    # If user has entered a symbol.      
    if request.method == 'POST' or request.args.get('sym'):
        symbol = request.form.get('symbol') if request.method == 'POST' else request.args.get('sym')
        view = request.form.get('view')
        if not view: view = 'Overview'
        symbol = symbol.upper()
        # Validate view
        if view not in views:
            flash('Invalid input.', category = 'warning')
            return redirect('quote')
        # If symbol already exits in the session variable, than there is no need to make an api call.
        if symbol in session:
            stock_info = session[symbol]
        # Otherwise make an api call.
        else: stock_info = lookup_symbol(symbol)
        if not stock_info:
            flash('Invalid symbol.', category = 'warning')
        else:
            # If the symbol is correct make sure it exists in our database.
            res = db.engine.execute(f'SELECT symbol FROM stock WHERE symbol = "{symbol}"')
            if not res:
                new_stock = Stock(symbol = symbol, company_name = stock_info[symbol]['company']["companyName"])
                db.session.add(new_stock)
                db.session.commit()
            # Add info to the session variable.
            session[symbol] = stock_info
            return render_template('quoted.html', stock_info = stock_info[symbol], view = view, views = views, datetime=datetime)
    return render_template('quote.html', views = views)


@app.route('/view')
@login_required(current_user, redirect)
def view():
    sym = request.args.get('sym')
    if sym not in session:
        return None
    return jsonify(session[sym][sym])


@app.route('/search')
@login_required(current_user, redirect)
def search():
    sym = request.args.get('sym')
    nm = request.args.get('nm')
    data, res = [], None
    # If user has entered a symbol, than search by symbol.
    if sym:
        res = db.engine.execute(f'SELECT * FROM stock WHERE stock.symbol LIKE "%{sym}%" LIMIT 70')
    # If user has entered a name, than search by name.
    elif nm:
        res = db.engine.execute(f'SELECT * FROM stock WHERE stock.company_name LIKE "%{nm}%" LIMIT 70')
    # If no symbol provided, than return the first 70 stocks.
    if not res:
        res = db.engine.execute(f'SELECT * FROM stock LIMIT 70')
    # Convert the data into a list of dictionaries.
    for symbol, name in res:
        data.append({'symbol': symbol, 'name': name})
    # Return the result in JSON format.
    return jsonify(data)


@app.route('/search_ownership')
@login_required(current_user, redirect)
def search_ownership():
    sym = request.args.get('sym')
    nm = request.args.get('nm')
    data, res = [], None
    # If user has entered a symbol, than search by symbol.
    if sym:
        res = db.engine.execute(f'SELECT logo, stock_id, shares FROM stocks__owned WHERE user_id = {current_user.id} AND stock_id LIKE "%{sym}%"')
    # If user has entered a name, than search by name.
    elif nm:
        res = db.engine.execute(f'SELECT logo, stock_id, shares \
                                  FROM stocks__owned \
                                  JOIN stock ON \
                                  stocks__owned.stock_id = stock.symbol \
                                  WHERE user_id = {current_user.id} AND stock.company_name LIKE "%{nm}%"')
    # If no symbol provided, than return all stocks currently owned by the user.
    if not res:
        res = db.engine.execute(f'SELECT logo, stock_id, shares FROM stocks__owned WHERE user_id = {current_user.id}')
    # Convert the data into a list of dictionaries.
    for logo, stock_id, shares in res:
        data.append({'logo': logo, 'stock_id': stock_id, 'shares': shares})
    # Return the result in JSON format.
    return jsonify(data)
    

@app.route('/buy', methods = ['GET', 'POST'])
@login_required(current_user, redirect)
def buy():
    form = PurchaseForm()
    symbol = request.args.get('sym')
    # Make sure symbol exists in session variable.
    if symbol not in session:
        stock_info = lookup_symbol(symbol)
        session[symbol] = stock_info
    stock_info = session[symbol][symbol]
    if form.validate_on_submit():
        if 'submit' not in request.form:
            return redirect(url_for('portfolio'))
        shares = int(request.form.get('shares'))
        price = float(stock_info['quote']['latestPrice'])
        # Compute the total cost of purchasing the stocks.
        total = shares * price

        # Find the balance of the user.
        balance = current_user.cash
        
        # If the available balance is less than the cost than cancel transaction.
        if balance < total:
            flash(f'Insufficient Balance!', category = 'primary')
            return redirect('/portfolio')

        # Otherwise deduct the amount from the current balance.
        current_user.cash -= total

        # Update ownership.
        stock = Stocks_Owned.query.filter_by(user_id = current_user.id, stock_id = stock_info['quote']['symbol']).first()
        # If user already owns this stock than update it.
        if stock:
            stock.shares += shares
        # Otherwise add it to the db
        else:
            stock_owned = Stocks_Owned(user_id = current_user.id, stock_id = stock_info['quote']['symbol'], shares = shares, logo = stock_info['logo']['url'])
            db.session.add(stock_owned)

        # Record the transaction.
        transaction = Transaction(user_id = current_user.id, stock_id = stock_info['quote']['symbol'], shares = shares, price = price)
        transaction.transacted = datetime.now()
        transaction.logo = stock_info['logo']['url']
        db.session.add(transaction)
        db.session.commit()

        flash(f"Purchased {shares} stocks of {stock_info['company']['companyName']} for ${total}", category = 'success')
        return redirect('/portfolio')
        
    elif form.errors != {}:
        if 'submit' not in request.form:
            return redirect(url_for('quote'))
        for category, err_msgs in form.errors.items():
            for err_msg in err_msgs:
                flash(f'There was an error: {err_msg}', category = 'danger')

    return render_template('buy.html', form = form, stock_info = stock_info)


@app.route('/sell', methods = ['GET', 'POST'])
@login_required(current_user, redirect)
def sell():
    form = SellForm()
    symbol = request.args.get('sym')
    # Make sure symbol exists in session variable.
    if symbol not in session:
        stock_info = lookup_symbol(symbol)
        session[symbol] = stock_info
    stock_info = session[symbol][symbol]
    if form.validate_on_submit():
        if 'submit' not in request.form:
            return redirect(url_for('portfolio'))
        shares = int(request.form.get('shares'))

        # Make sure the user actually has these many shares.
        stock = Stocks_Owned.query.filter_by(user_id = current_user.id, stock_id = stock_info['quote']['symbol']).first()
        if not stock or stock.shares < shares:
            flash(f"Insufficient shares!", category = 'primary')
            return redirect('/quote')

        # Get the current price of stock.
        price = float(stock_info['quote']['latestPrice'])

        # Compute the total cost of selling the stocks.
        total = shares * price

        # Update the number of stocks.
        stock.shares -= shares

        # If the number of shares is 0 than remove it from the db.
        if stock.shares == 0:
            db.session.delete(stock)

        # Update the balance of the user.
        current_user.cash += total

        # Record the transaction.
        transaction = Transaction(user_id = current_user.id, stock_id = stock_info['quote']['symbol'], shares = -1 * shares, price = price)
        transaction.transacted = datetime.now()
        transaction.logo = stock_info['logo']['url']
        db.session.add(transaction)
        db.session.commit()
        flash(f"Sold {shares} stocks of {stock_info['company']['companyName']} for ${total}", category = 'success')
        return redirect('/portfolio')
        
    elif form.errors != {}:
        if 'submit' not in request.form:
            return redirect(url_for('quote'))
        for category, err_msgs in form.errors.items():
            for err_msg in err_msgs:
                flash(f'There was an error: {err_msg}', category = 'danger')

    return render_template('sell.html', form = form, stock_info = stock_info)



@app.route('/portfolio')
@login_required(current_user, redirect)
def portfolio():
    # Get all the stocks owned by the user.
    views = ['shares', 'amount']
    periods = ['1y', '2y', '3y', '4y', '5y', '10y', '15y']
    types = ['Candlestick', 'Lines', 'Scatter', 'Lines_scatter', 'Bar']
    stocks = Stocks_Owned.query.filter_by(user_id = current_user.id).all()
    if not stocks:
        flash("You currently don't own any shares. Start investing today!", category = 'warning')
        return redirect('/quote')
    return render_template('portfolio.html', stocks = stocks, types = types, views = views, periods = periods)


@app.route('/plot_overview_shares')
@login_required(current_user, redirect)
def plot_overview_shares():
    stocks = Stocks_Owned.query.filter_by(user_id = current_user.id).all()
    values, labels = [], []
    for stock in stocks:
        values.append(stock.shares)
        labels.append(stock.stock_id)
    val = pyo.plot({"data": [go.Pie(values = values, labels = labels)]
          , "layout": go.Layout(title = 'Overview', margin = dict(l = 10, r = 10, t = 30, b = 30))
          }, output_type='div')
    data = {'file': val}
    return jsonify(data)


@app.route('/plot_overview_amount')
@login_required(current_user, redirect)
def plot_overview_amount():
    stocks = Stocks_Owned.query.filter_by(user_id = current_user.id).all()
    values, labels = [], []
    for stock in stocks:
        values.append(stock.shares)
        labels.append(stock.stock_id)
    # Get the latest price of all the stocks owned by the user.
    for i in range(len(labels)):
        if labels[i] in session:
            quote = session[labels[i]]
        else: 
            quote = lookup_symbol(labels[i])
            session[labels[i]] = quote
        values[i] = values[i] * quote[labels[i]]['quote']['latestPrice']
    val = pyo.plot({"data": [go.Pie(values = values, labels = labels)]
          , "layout": go.Layout(title = 'Overview', margin = dict(l = 10, r = 10, t = 30, b = 30))
          }, output_type='div')
    data = {'file': val}
    return jsonify(data)


@app.route('/plot_candlestick')
@login_required(current_user, redirect)
def plot_candlestick():
    sym = request.args.get('sym')
    prd = request.args.get('prd')
    ticker = yfinance.Ticker(sym)
    hist = ticker.history(period = prd)
    div = pyo.plot({"data": [go.Candlestick(x = hist.index, open = hist['Open'], high = hist['High'], low = hist['Low'], close = hist['Close'])]
                    ,"layout": go.Layout(title = sym, margin = dict(l=0, r=0, t=30, b=30))
                    }, output_type='div')
    data = {'file': div}
    return jsonify(data)


@app.route('/plot_lines')
@login_required(current_user, redirect)
def plot_lines():
    sym = request.args.get('sym')
    prd = request.args.get('prd')
    ticker = yfinance.Ticker(sym)
    hist = ticker.history(period = prd)
    div = pyo.plot({"data": [go.Scatter(x = hist.index, y = hist['Close'], mode = 'lines')]
                    ,"layout": go.Layout(title = sym, margin = dict(l=0, r=0, t=30, b=30))
                    }, output_type='div')
    data = {'file': div}
    return jsonify(data)


@app.route('/plot_scatter')
@login_required(current_user, redirect)
def plot_scatter():
    sym = request.args.get('sym')
    prd = request.args.get('prd')
    ticker = yfinance.Ticker(sym)
    hist = ticker.history(period = prd)
    div = pyo.plot({"data": [go.Scatter(x = hist.index, y = hist['Close'], mode = 'markers')]
                    ,"layout": go.Layout(title = sym, margin = dict(l=0, r=0, t=30, b=30))
                    }, output_type='div')
    data = {'file': div}
    return jsonify(data)


@app.route('/plot_lines_scatter')
@login_required(current_user, redirect)
def plot_lines_scatter():
    sym = request.args.get('sym')
    prd = request.args.get('prd')
    ticker = yfinance.Ticker(sym)
    hist = ticker.history(period = prd)
    div = pyo.plot({"data": [go.Scatter(x = hist.index, y = hist['Close'], mode = 'lines+markers')]
                    ,"layout": go.Layout(title = sym, margin = dict(l=0, r=0, t=30, b=30))
                    }, output_type='div')
    data = {'file': div}
    return jsonify(data)


@app.route('/plot_bar')
@login_required(current_user, redirect)
def plot_bar():
    sym = request.args.get('sym')
    prd = request.args.get('prd')
    ticker = yfinance.Ticker(sym)
    hist = ticker.history(period = prd)
    div = pyo.plot({"data": [go.Bar(x = hist.index, y = hist['Close'])]
                    ,"layout": go.Layout(title = sym, margin = dict(l=0, r=0, t=30, b=30))
                    }, output_type='div')
    data = {'file': div}
    return jsonify(data)


@app.route('/history')
@login_required(current_user, redirect)
def history():
    views = ['Recent', 'Old']
    transactions = Transaction.query.filter_by(user_id = current_user.id).order_by(Transaction.transacted.desc()).all()
    if not transactions:
        flash("You haven't carried out any transactions.", category = 'warning')
    return render_template('history.html', transactions = transactions, views = views)


@app.route('/history_sym')
@login_required(current_user, redirect)
def history_sym():
    sym = request.args.get('sym')
    transactions = Transaction.query.filter_by(user_id = current_user.id and Transaction.stock_id.like('%'+ sym +'%')).order_by(Transaction.transacted.desc()).all()
    data = []
    for transaction in transactions:
        data.append({'logo': transaction.logo, 'sym': transaction.stock_id, 'shares': transaction.shares, 'price': transaction.price, 'datetime': transaction.transacted})
    return jsonify(data)


@app.route('/history_sort')
@login_required(current_user, redirect)
def history_sort():
    sort = request.args.get('sort')
    if sort == 'Old':
        transactions = Transaction.query.filter_by(user_id = current_user.id).order_by(Transaction.transacted).all()
    elif sort == 'Recent':
        transactions = Transaction.query.filter_by(user_id = current_user.id).order_by(Transaction.transacted.desc()).all()
    else: 
        flash('Invalid request!', category = 'danger')
        return redirect('/history')
    data = []
    for transaction in transactions:
        data.append({'logo': transaction.logo, 'sym': transaction.stock_id, 'shares': transaction.shares, 'price': transaction.price, 'datetime': transaction.transacted})
    return jsonify(data)


@app.route('/profile')
@login_required(current_user, redirect)
def profile():
    stocks_owned = Stocks_Owned.query.filter_by(user_id = current_user.id).all()
    periods = ['1y', '2y', '3y', '4y', '5y', '10y', '15y']
    symbols = []
    stocks = []
    for stock in stocks_owned:
        if stock.stock_id not in session:
            stock_info = lookup_symbol(stock.stock_id)
            session[stock.stock_id] = stock_info
        symbols.append(stock.stock_id)
        stock_price = session[stock.stock_id][stock.stock_id]['quote']['latestPrice']
        total = stock_price * stock.shares
        stocks.append({'logo': stock.logo, 'symbol': stock.stock_id, 'shares': stock.shares, 'price': stock_price, 'total': '{:.4f}'.format(total)})
    return render_template('profile.html', stocks = stocks, symbols = symbols, periods = periods)


@app.route('/plot_moving_avg')
@login_required(current_user, redirect)
def plot_moving_avg():
    sym = request.args.get('sym')
    prd = request.args.get('prd')
  
    ticker = yfinance.Ticker(sym)
    hist = ticker.history(period = prd)
    hist['100MA'] = hist['Close'].rolling(window = 100).mean()
    hist['200MA'] = hist['Close'].rolling(window = 200).mean()

    div = pyo.plot({"data": go.Figure(data = go.Scatter(x = hist.index, y = hist['Close'], mode = 'lines') ).add_trace(
                            go.Scatter(x = hist.index, y = hist['200MA'], line = dict(color = 'green'), name = '100MA')
                        ).add_trace(
                            go.Scatter(x = hist.index, y = hist['100MA'], line = dict(color = 'red'), name = '200MA')
                        ),
                "layout": go.Layout(title = sym, margin = dict(l=0, r=0, t=30, b=30), )
               }, output_type='div')
    data = {'file': div}
    return jsonify(data)


@app.route('/get_prediction')
@login_required(current_user, redirect)
def get_prediction():
    sym = request.args.get('sym')
    prd = request.args.get('prd')
    prd = int(prd[0 : len(prd) - 1])
    data = predict(symbol = sym, period = prd)
    return jsonify(data)