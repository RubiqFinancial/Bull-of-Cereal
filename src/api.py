from flask import Flask, request
# from flask_restful import Resource, Api, reqparse
from exchanges import exchangemanager, exchange
from trade_engine import coin, candle, engine
import pandas as pd

app = Flask(__name__)
engine = None
xc_manager = exchangemanager.ExchangeManager()

@app.route('/api', methods=['GET'])
def api_get():
    return "Welcome to the RubiqCapital API"

# exchanges endpoint
@app.route('/api/exchanges', methods=['GET'])
# get method: gets exchange account info like positions, liquidity, margin, etc
def exchanges_get():
    """
    get info from exchanges
    universal get parameters (? means optional)

    account: string (ex: 'Kucoin') ?
    margin_account: string (ex: 'Kucoin') ?
    symbol: string (ex: BTCUSDT) ?
    """

    args = dict(request.args)
    return_dict = {}
    xcs = [xc.get_name().value for xc in xc_manager.get_exchanges()]

    # if no parameters, then just list exchanges
    if len(args) == 0:
        return {'exchanges': xcs}, 200

    # if param is account
    if 'account' in args:
        xc_str = args['account']
        if xc_str not in xcs:
            return {"error": "exchange invalid"}

        account_info = xc_manager.get_exchange(exchange.ExchangeName.KUCOIN).get_account_info()
        if account_info is None:
            return "There was a problem getting your account information"

        if "error" not in account_info:
            # if param is symbol
            if 'symbol' in args:
                pass

        return_dict['account_info'] = account_info

    # if param is margin_account
    if 'margin_account' in args:
        xc_str = args['margin_account']
        if xc_str not in xcs:
            return {"error": "exchange invalid"}

        margin_account = {'margin_account_info': 'invalid exchange'}
        if xc_str == exchange.ExchangeName.KUCOIN.value:
            margin_account = xc_manager.get_exchange(exchange.ExchangeName.KUCOIN).get_margin_account_info()
            if margin_account is None:
                return "there was a problem getting your account information"

            if "error" not in account_info:
                # if param is symbol
                if 'symbol' in args:
                    pass

        return_dict['margin_account'] = margin_account

    return return_dict, 200

@app.route('/api/exchanges', methods=['POST'])
def exchanges_post():
    """
    post trades etc
    universal post parameters (? means optional)

    exchange: string (ex: 'Kucoin')
    action: string (ex: 'buy')
    quote: string (ex: 'BTC')
    base: string (ex: 'USDT')
    amount_base: float (ex: 1040.39)
    """

    request_data = request.get_json()
    if request_data is None:
        return 'error: no body', 200

    if 'exchange' in request_data:
        exchange = request_data['exchange']

    if 'action' in request_data:
        action = request_data['action']

    if 'base' in request_data:
        base = request_data['base']

    if 'quote' in request_data:
        quote = request_data['quote']

    if 'amount' in request_data:
        amount = request_data['amount']

    return {'received': request_data}, 200


# autoview alerts endpoint
@app.route('/api/alerts/autoview', methods=['POST'])
def autoview_post():
    """
    autoview alerts
    univeral post parameters (all are optional)

    key     type    default     values                  name                        description
    ----------------------------------------------------------------------------------------------------------
    a:      str     *           [A-Za-z0-9]             account                     alias for API creds
    ac:     int                 [0-9]                   alert count
    amr:    int     0           0,1                     auto margin replenishment   Bitget: available funds will transfer to margin of the position
    b:      str     all         buy, sell, long, short  book                        sides of the market to play
    bcc:    int     0           0,1                     blind carbon copy           relay to configured endpoint, not exchange requests made
    c:      str?    n/a         order, position         cancel/close                cancel open orders or close open positions
    cbr:    float   0.1         > 0.1                   callback rate               binance futures/testnet: % value
    cc:     int     0           0,1                     carbon copy                 relay to configured enpoint and exchange
    cm:     str?    all         static: #, %            cancel/close max            cancels orders or closes positions
                                random: #-#, %-%
    cmo:    str?    oldest      newest, oldest, lowest  cancel/close max order      how the orders are sorted for canceling
                                highest, smallest                                   how the positions are sorted for closing
                                biggest, random                                     Kucoin: adjust repaying strategy from recently expiring to
                                                                                            rate first (ex: y=repay, cmo=highest)
    cot:    int     0           0,1                     close on trigger            ByBit/testnet: when creating a closing order, use this to avoid
                                                                                                   failing by insufficient available margin
    d:      int     0           0,1                     disabled                    prevents live action from command (debugging)
    delay:  float   n/a         > 0                     delay                       pause (seconds) between commands in the same alert
    dt:     time    n/a         ex: 2020-0-14           date/time                   OANDA/practice date/time when (open) order is cancelled
    e:      str     n/a         Kucoin, Bitrue...       exchange                    receiving exchange for command
    f:      int     0           0,1                     fee                         switch trading fee to exchange provided
    fgsl:   str?    n/a         static: #, random: #-#  fixed guaranteed stop loss  OANDA/practice order created with price threshold guaranteed against loss
    fp:     str?    n/a         static: #, random: #-#  fixed price                 the literal price in which to place an order or close a position
    fpx:                                                fixed trigger price
    fsl:    str?    n/a         static: #, random: #-#  fixed stop loss             Kraken: triggers the order when the last traded price hits the stop price
    ftp:                                                fixed take profit
    fts:                                                fixed trailing stop
    gsl:                                                guaranteed stop loss
    h:                                                  hidden/iceberg
    l:                                                  leverage
    lt:                                                 leverage type
    oco:                                                one cancels the other
    p:                                                  price
    ps:                                                 price source
    px:                                                 trigger price
    pxs:                                                trigger price source
    q:                                                  quantity
    ro:                                                 reduce only
    s:                                                  symbol
    sl:                                                 stop loss
    t:                                                  order type
    testing:                                            testing
    tp:                                                 take profit
    ts:                                                 trailing stop
    u:                                                  unit
    v:                                                  version
    w:                                                  wallet
    y:                                                  yield
    """

    request_data = request.get_json()

    print(request_data)
    return {'received': request_data}, 200

# tradingview alerts endpoint
@app.route('/api/alerts/tradingview', methods=['GET'])
# get alert details - not sure how this will work or if it will work at all
def tradingview_get():
    return {'alert info': 'much wow'}, 200

# post alerts from tradingview here
@app.route('/api/alerts/tradingview', methods=['POST'])
def tradingview_post():


    return {'r': 'ack'}, 200

# @app.route('/api/engine', methods=['POST'])
# def engine_post():
#     request_data = request.get_json()
#     args = list(request.args)
#
#     if 'initcoins' in args:
#         return {"initializing local api engine coins": request_data}
#
#     return {'params': args, 'json data': request_data}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
