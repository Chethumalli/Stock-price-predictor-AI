from flask import Flask, render_template, request, jsonify
from groq import Groq
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()
    ticker = data["ticker"]

    # Get stock data
    stock = yf.download(ticker, period="1y")

    prices = stock["Close"].dropna().values
    dates = stock.index.strftime('%Y-%m-%d').tolist()

    X = np.arange(len(prices)).reshape(-1,1)
    y = prices

    model = LinearRegression()
    model.fit(X,y)

    next_day = np.array([[len(prices)]])
    prediction = model.predict(next_day)[0]

    current_price = prices[-1]

    # Buy/Sell Signal
    if prediction > current_price:
        signal = "BUY"
    elif prediction < current_price:
        signal = "SELL"
    else:
        signal = "HOLD"

    # AI Analysis
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"Give a short investment analysis and outlook for stock {ticker}"
            }
        ]
    )

    analysis = response.choices[0].message.content

    return jsonify({
        "prediction": round(float(prediction),2),
        "current_price": round(float(current_price),2),
        "signal": signal,
        "analysis": analysis,
        "prices": prices.tolist(),
        "dates": dates
    })
if __name__ == "__main__":
    app.run(debug=True)