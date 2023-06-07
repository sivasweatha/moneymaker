import requests
import pytest
from datetime import datetime as dt
from imports import OrderPlacer
from imports import stockExchangeMap
from imports import vendors
from unittest.mock import patch

def test_maps_keyerror():
    orderplacer = OrderPlacer(None, None)
    with pytest.raises(SystemExit):
        orderplacer.check_stock_mappings()

def test_maps():
    stocks = stockExchangeMap.keys()
    for stock in stocks:
        orderplacer = OrderPlacer(stock, None)
        assert orderplacer.check_stock_mappings() == None

def test_market_hours_us():
    current_time = dt.now().hour * 100 + dt.now().minute
    us_stocks = list(filter(lambda stock: stockExchangeMap[stock] == "US", stockExchangeMap))

    if current_time < 125:
    # 0:00 to 1:25
        for stock in us_stocks:
            orderplacer = OrderPlacer(stock, None)
            assert orderplacer.check_trading_hours() == None
    elif current_time > 1900:
    # 19:00 to 23:59
        for stock in us_stocks:
            orderplacer = OrderPlacer(stock, None)
            assert orderplacer.check_trading_hours() == None
    else:
        for stock in us_stocks:
            orderplacer = OrderPlacer(stock, None)
            with pytest.raises(SystemExit):
                orderplacer.check_trading_hours()

def test_market_hours_in():
    current_time = dt.now().hour * 100 + dt.now().minute
    in_stocks = list(filter(lambda stock: stockExchangeMap[stock] == "IN", stockExchangeMap))

    if 915 < current_time < 1530:
    # 9:15 to 15:30
        for stock in in_stocks:
            orderplacer = OrderPlacer(stock, None)
            assert orderplacer.check_trading_hours() == None
    else:
        for stock in in_stocks:
            orderplacer = OrderPlacer(stock, None)
            assert orderplacer.check_trading_hours() == None

def test_downloading_invalid_data():
    orderplacer = OrderPlacer(None, None)
    with pytest.raises(SystemExit):
        orderplacer.download_strategy_data()

def test_downloading_data():
    stocks = stockExchangeMap.keys()
    for stock in stocks:
        orderplacer = OrderPlacer(stock, None)
        assert orderplacer.download_strategy_data() == None

def test_papercookie_validity():
    with patch('vendors.tradingviewPaperTrader.PaperTrade') as mock_papertrade:
        mock_papertrade_instance = mock_papertrade.return_value
        mock_papertrade_instance.checkCookieValidity.return_value = True
        orderplacer = OrderPlacer(None, None)
        orderplacer.pt = mock_papertrade_instance
        assert orderplacer.check_tradingview_cookie() == None

def test_papercookie_invalidity():
    with patch('vendors.tradingviewPaperTrader.PaperTrade') as mock_papertrade:
        mock_papertrade_instance = mock_papertrade.return_value
        mock_papertrade_instance.checkCookieValidity.return_value = False
        orderplacer = OrderPlacer(None, None)
        orderplacer.pt = mock_papertrade_instance
        with pytest.raises(SystemExit):
            orderplacer.check_tradingview_cookie()