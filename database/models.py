import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from pydantic import BaseModel, ConfigDict, Field

class OLHC(BaseModel):
    __table_name__ = "ohlc"
    
    time: int = sa.Column(sa.Integer,nullable=False)
    symbol: str = sa.Column(sa.String(10),nullable=False)
    resolution: str = sa.Column(sa.String(10),nullable=False)
    lastUpdated: int = sa.Column(sa.Integer,nullable=False)
    type: str = sa.Column(sa.String(8),nullable=False)
    open: float = sa.Column(sa.Integer,nullable=False)
    low: float = sa.Column(sa.Float,nullable=False)
    high: float = sa.Column(sa.Float,nullable=False)
    close: float = sa.Column(sa.Float,nullable=False)
    volume: float = sa.Column(sa.Float,nullable=False)

    __table_args__ = (
        sa.UniqueConstraint('time', 'symbol', name='idx_ohlc'),
    )


class StockInfo(BaseModel):
    __table_name__ = "stock_info"

    # {"floorCode":"HOSE","symbol":"CMWG2504","tradingTime":"2025-04-29T08:43:17.718240739Z","securityType":"COVERED_WARRANT","basicPrice":1.92,"ceilingPrice":2.76,"floorPrice":1.08,"highestPrice":2.0,"lowestPrice":1.94,"avgPrice":1.96,"sellForeignQtty":2780.0,"currentRoom":497100.0,"accumulatedVal":0.1580810000000001,"accumulatedVol":8050.0,"matchPrice":1.98,"matchQtty":890.0,"changed":0.06,"changedRatio":3.13,"estimatedPrice":1.98,"tradingSession":"CLOSED","securityStatus":"NORMAL","oddLotSecurityStatus":"HALT"}
    
    floorCode: str = sa.Column(sa.String(10), nullable=False)
    symbol: str = sa.Column(sa.String(10), nullable=False)
    tradingTime: str =  sa.Column(sa.TIMESTAMP(timezone=False),nullable=False)
    securityType: str = sa.Column(sa.String(20), nullable=False)
    basicPrice: float = sa.Column(sa.Float, nullable=False)
    ceilingPrice: float = sa.Column(sa.Float, nullable=False)
    floorPrice: float = sa.Column(sa.Float, nullable=False)
    highestPrice: float = sa.Column(sa.Float, nullable=False)
    lowestPrice: float = sa.Column(sa.Float, nullable=False)
    avgPrice: float = sa.Column(sa.Float, nullable=False)
    buyForeignQtty: float = sa.Column(sa.Float, nullable=False)
    sellForeignQtty: float = sa.Column(sa.Float, nullable=False)
    currentRoom: float = sa.Column(sa.Float, nullable=False)
    accumulatedVal: float = sa.Column(sa.Float, nullable=False)
    accumulatedVol: float = sa.Column(sa.Float, nullable=False)
    matchPrice: float = sa.Column(sa.Float, nullable=False)
    matchQtty: float = sa.Column(sa.Float, nullable=False)
    changed: float = sa.Column(sa.Float, nullable=False)
    changedRatio: float = sa.Column(sa.Float, nullable=False)
    estimatedPrice: float = sa.Column(sa.Float, nullable=False)
    tradingSession: str = sa.Column(sa.String(10), nullable=False)
    securityStatus: str = sa.Column(sa.String(10), nullable=False)
    oddLotSecurityStatus: str = sa.Column(sa.String(10), nullable=False)

    __table_args__ = (
        sa.UniqueConstraint('symbol',"tradingTime", name='idx_stock_info'),
    )

class MarketIndex(BaseModel):
    __table_name__ = "market_index"

    marketID: str = sa.Column(sa.String(10), nullable=False)
    totalTrade: float = sa.Column(sa.Float, nullable=False)
    totalShareTraded: float = sa.Column(sa.Float, nullable=False)
    totalValueTraded: float = sa.Column(sa.Float, nullable=False)
    advance: float = sa.Column(sa.Float, nullable=False)
    decline: float = sa.Column(sa.Float, nullable=False)
    noChange: float = sa.Column(sa.Float, nullable=False)
    indexValue: float = sa.Column(sa.Float, nullable=False)
    changed: float = sa.Column(sa.Float, nullable=False)
    tradingTime: str = sa.Column(sa.TIMESTAMP(timezone=False), nullable=False)
    tradingDate: str = sa.Column(sa.TIMESTAMP(timezone=False), nullable=False)
    floorCode: str = sa.Column(sa.String(10), nullable=False)
    marketIndex: float = sa.Column(sa.Float, nullable=False)
    priorMarketIndex: float = sa.Column(sa.Float, nullable=False)
    highestIndex: float = sa.Column(sa.Float, nullable=False)
    lowestIndex: float = sa.Column(sa.Float, nullable=False)
    indexName: str = sa.Column(sa.String(10), nullable=False)
    tradingSessionId: str = sa.Column(sa.String(10), nullable=False)

    __table_args__ = (
        sa.UniqueConstraint('marketID', 'tradingDate', name='idx_market_index'),
    )