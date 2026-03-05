import yfinance as yf

def get_stock_info(ticker):

    stock = yf.Ticker(ticker)

    info = stock.info

    data = {
        "company": info.get("longName"),
        "sector": info.get("sector"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "summary": info.get("longBusinessSummary")
    }

    return data