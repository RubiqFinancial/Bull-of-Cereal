import pprint

alert = {
    # options binance
    "Exchange": "binance",
    # a1 corresponds to a1 account in binance
    "Account": "a1",
    # True or False
    "Testing": False,
    "Symbol": "BTCUSDT",
    "ModifyLeverage": False,
    "Leverage": 100,
    # CROSSED /ISOLATED
    "ModifyLeverageType": False,
    "LeverageType": "CROSSED",
    "CancelAllOpenOrders": False,
    # options LIMIT/ MARKET/ STOP_MARKET/ STOP_LIMIT/ TAKE_PROFIT_LIMIT/ TAKE_PROFIT_MARKET
    "OrderType": "LIMIT",
    "Oco": True,
    # options Buy/ Sell
    "Side": "Buy",
    # needed for all limit order types
    "Price": 39000,
    "Quantity": 0.001,
    # used only when ordertype is relevant
    "BasePrice": 36000,
    "Trigger_by": "LastPrice",
    # take profit price
    "TakeProfitPrice": 41000,
    # stop loss price
    "StopLossPrice": 33000,
    "ReduceOnly": False,
    # options GoodTillCancel, ImmediateOrCancel, FillOrKill, PostOnly
    "TimeInForce": "GoodTillCancel",
    "CloseOnTrigger": False,
    "ClosePosition": False,
    # CONTRACT_PRICE, MARK_PRICE
    "WorkingType": "CONTRACT_PRICE",
    "PriceProtect": False,
}