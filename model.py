import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_price(ticker):

    try:

        data = yf.download(ticker, period="1y", progress=False)

        if data.empty:
            return 0, None

        data["Prediction"] = data["Close"].shift(-1)

        X = np.array(data[["Close"]][:-1])
        y = np.array(data["Prediction"][:-1])

        model = LinearRegression()
        model.fit(X, y)

        last_price = np.array(data[["Close"]].tail(1))

        predicted = model.predict(last_price)

        return float(predicted[0]), data

    except Exception as e:

        print("Stock error:", e)
        return 0, None