STOCK_LIST = [
    "HPG",
    "VCB",
    "VHM",
    "VNM",
    "FPT",
    "MWG",
    "VRE",
    "GVR",
]


INDEX_LIST = ["VN30", "VNINDEX"]

def stock_topics(symbol):
    """
    Generate stock topics for the given stock symbol.
    """
    return f"plaintext/quotes/stock/SI/{symbol}"

def index_topics(index):
    """
    Generate index topics for the given index.
    """
    return f"plaintext/quotes/index/MI/{index}"

def olhc_topics_1H(symbol):
    """
    Generate OHLC topics for the given stock symbol.
    """
    return f"plaintext/quotes/stock/OHLC/1H/{symbol}"