import yfinance
from prophet import Prophet
import plotly.graph_objects as go
from datetime import date
from prophet.plot import plot_plotly
import plotly.offline as pyo

PERIOD = '5y'

# Period is in years.
def predict(symbol, period):
    # Create a ticker object.
    stock = yfinance.Ticker(symbol)

    # Get historic data.
    data = stock.history(period = PERIOD)
    data.reset_index(inplace = True)

    # No of days.
    n_days = period * 365

    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns = {'Date': 'ds', 'Close': 'y'})

    # Create a model.
    model = Prophet()
    model.fit(df_train)

    # Predict
    future = model.make_future_dataframe(periods = n_days)
    forcast = model.predict(future)

    # Plot
    fig2 = plot_plotly(model, forcast)

    # Return as div
    div = pyo.plot({'data' : fig2, 'layout' : go.Layout(title = symbol, margin = dict(l=0, r=0, t=30, b=30), )}, output_type = 'div')

    # return as a dictionary
    return {'plot' : div}
