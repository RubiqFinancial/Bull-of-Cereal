import bybit
import pandas as pd
import config_file
import os

# Inverse Perpetual
# interval has to be number of minutes and start as unix timestamp fetch_kline_data('BTCUSD', '1', 1615067100)
def fetch_ip_kline_data(client, symbol, interval, start):
    data = client.Kline.Kline_get(symbol=symbol, interval=str(interval), **{'from':start}).result()[0]['result']
    return pd.DataFrame(data)

# interval has to be number of minutes and start as unix timestamp
def fetch_ip_kline_markprice_data(client, symbol, interval, start):
    data = client.Kline.Kline_markPrice(symbol=symbol, interval=str(interval), **{'from':start}).result()[0]['result']
    return pd.DataFrame(data)

# interval has to be number of minutes and start as unix timestamp
def fetch_ip_kline_indexprice_data(client, symbol, interval, start):
    data = client.Kline.Kline_indexPrice(symbol=symbol, interval=str(interval), **{'from':start}).result()[0]['result']
    return pd.DataFrame(data)

# interval has to be number of minutes and start as unix timestamp
def fetch_ip_kline_premiumindexPrice_data(client, symbol, interval, start):
    data = client.Kline.Kline_premiumIndexPrice(symbol=symbol, interval=str(interval), **{'from':start}).result()[0]['result']
    return pd.DataFrame(data)

# get symbol details bid/ ask price, last price, mark price, funding rate, 24h prices, open interest, funding rate etc.
def get_ip_symbol_info(client, symbol):
    data = client.Market.Market_symbolInfo().result()[0]['result']
    return list(filter(lambda x: x['symbol'] == symbol, data))

# get trading rules like fee, leverage, minimum price, tick size etc
def get_ip_symbol_trading_rules(client, symbol):
    data = client.Symbol.Symbol_get().result()[0]['result']
    return list(filter(lambda x: x['name'] == symbol, data))

# limit in integers and period e.g. "5min"
def get_ip_buy_sell_ratio(client, symbol, limit, period):
    return client.Market.Market_accountRatio(symbol=symbol, limit=limit, period=period).result()[0]['result']

# Place Active Order
def place_ip_limit_buy(client, symbol, qty, price, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.Order.Order_new(side="Buy",symbol=symbol,order_type="Limit",qty=qty,price=price,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger).result()

def place_ip_limit_sell(client, symbol, qty, price, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.Order.Order_new(side="Sell",symbol=symbol,order_type="Limit",qty=qty,price=price,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger).result()

# stop loss and take profit are market orders
def place_ip_limit_buy_oco(client, symbol, qty, price, tp_price, sl_price, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.Order.Order_new(side="Buy",symbol=symbol,order_type="Limit",qty=qty,price=price,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger, take_profit=tp_price, stop_loss = sl_price).result()

def place_ip_limit_sell_oco(client, symbol, qty, price, tp_price, sl_price, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.Order.Order_new(side="Sell",symbol=symbol,order_type="Limit",qty=qty,price=price,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger, take_profit=tp_price, stop_loss = sl_price).result()

def place_ip_market_buy(client, symbol, qty, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.Order.Order_new(side="Buy",symbol=symbol,order_type="Market",qty=qty,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger).result()

def place_ip_market_sell(client, symbol, qty, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.Order.Order_new(side="Sell",symbol=symbol,order_type="Market",qty=qty,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger).result()

def place_ip_market_buy_oco(client, symbol, qty, tp_price, sl_price, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.Order.Order_new(side="Buy",symbol=symbol,order_type="Market",qty=qty,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger, take_profit=tp_price, stop_loss = sl_price).result()

def place_ip_market_sell_oco(client, symbol, qty, tp_price, sl_price, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.Order.Order_new(side="Sell",symbol=symbol,order_type="Market",qty=qty,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger, take_profit=tp_price, stop_loss = sl_price).result()

# Get order history
def get_ip_orders(client, symbol):
    return client.Order.Order_getOrders(symbol=symbol).result()[0]['result']

def cancel_ip_order(client, symbol, order_id):
    return client.Order.Order_cancel(symbol=symbol, order_id=order_id).result()[0]['result']

def cancel_ip_all_orders(client, symbol):
    return client.Order.Order_cancelAll(symbol=symbol).result()[0]['result']

def get_ip_order_status(client, symbol, order_id):
    return client.Order.Order_query(symbol=symbol, order_id=order_id).result()[0]['result']

def amend_ip_order_qty(client, symbol, order_id, new_qty):
    return client.Order.Order_replace(symbol=symbol, order_id=order_id, p_r_qty=str(new_qty)).result()[0]['result']

def amend_ip_order_price(client, symbol, order_id, new_price):
    return client.Order.Order_replace(symbol=symbol, order_id=order_id, p_r_price=str(new_price)).result()[0]['result']


def place_ip_limit_buy_conditional_order(client, symbol, qty, price, base_price, stop_price, tif = "GoodTillCancel", close_on_trigger = False):
    return client.Conditional.Conditional_new(order_type="Limit",side="Buy",symbol=symbol,qty=str(qty),price=str(price),
    base_price=str(base_price),stop_px=str(stop_price),time_in_force=tif, close_on_trigger=close_on_trigger).result()[0]['result']

def place_ip_limit_sell_conditional_order(client, symbol, qty, price, base_price, stop_price, tif = "GoodTillCancel", close_on_trigger = False):
    return client.Conditional.Conditional_new(order_type="Limit",side="Sell",symbol=symbol,qty=str(qty),price=str(price),
    base_price=str(base_price),stop_px=str(stop_price),time_in_force=tif, close_on_trigger=close_on_trigger).result()[0]['result']


def place_ip_market_buy_conditional_order(client, symbol, qty, base_price, stop_price, tif = "GoodTillCancel", close_on_trigger = False):
    return client.Conditional.Conditional_new(order_type="Market",side="Buy",symbol=symbol,qty=str(qty),
    base_price=str(base_price),stop_px=str(stop_price),time_in_force=tif, close_on_trigger=close_on_trigger).result()[0]['result']

def place_ip_market_sell_conditional_order(client, symbol, qty, base_price, stop_price, tif = "GoodTillCancel", close_on_trigger = False):
    return client.Conditional.Conditional_new(order_type="Market",side="Sell",symbol=symbol,qty=str(qty),
    base_price=str(base_price),stop_px=str(stop_price),time_in_force=tif, close_on_trigger=close_on_trigger).result()[0]['result']

def get_ip_untriggered_conditional_orders_history(client, symbol):
    return client.Conditional.Conditional_getOrders(symbol=symbol, stop_order_status="Untriggered").result()

# Cancel Conditional Order
def cancel_ip_conditional_order(client, symbol, order_id):
    return client.Conditional.Conditional_cancel(symbol="BTCUSD", order_id=order_id).result()[0]['result']

def cancel_ip_all_conditional_orders(client, symbol):
    return client.Conditional.Conditional_cancelAll(symbol="BTCUSD").result()[0]['result']

def get_ip_conditional_order_status(client, symbol, order_id):
    return client.Conditional.Conditional_query(symbol=symbol, stop_order_id=order_id).result()[0]['result']

def amend_ip_conditional_order_qty(client, symbol, order_id, new_qty):
    return client.Conditional.Conditional_replace(symbol=symbol, stop_order_id=order_id, p_r_qty=str(new_qty)).result()[0]['result']

def amend_ip_conditional_order_price(client, symbol, order_id, new_price):
    return client.Conditional.Conditional_replace(symbol=symbol, stop_order_id=order_id, p_r_price=str(new_price)).result()[0]['result']

def get_ip_position(client, symbol):
    return client.Positions.Positions_myPosition(symbol=symbol).result()[0]['result']

def change_ip_margin(client, symbol, margin):
    return client.Positions.Positions_changeMargin(symbol=symbol, margin=str(margin)).result()[0]['result']

def position_ip_trading_stop(client, symbol, tp_price, sl_price):
    return client.Positions.Positions_tradingStop(symbol=symbol, take_profit=str(tp_price), stop_loss=str(sl_price)).result()[0]['result']

def set_ip_leverage(client, symbol, leverage):
    return client.Positions.Positions_saveLeverage(symbol=symbol, leverage=leverage).result()[0]['result']

def get_ip_last_funding_rate(client, symbol):
    return client.Funding.Funding_myLastFee(symbol=symbol).result()[0]['result']

def get_ip_wallet_balance(client, coin):
    return client.Wallet.Wallet_getBalance(coin=coin).result()[0]['result']

# USDT Perpetual
# interval has to be number of minutes and start as unix timestamp fetch_kline_data('BTCUSD', '1', 1615067100)
def fetch_up_kline_data(client, symbol, interval, start):
    data = client.LinearKline.LinearKline_get(symbol=symbol, interval=str(interval), **{'from':start}).result()[0]['result']
    return pd.DataFrame(data)


# interval has to be number of minutes and start as unix timestamp
def fetch_up_kline_markprice_data(client, symbol, interval, start):
    data = client.LinearKline.LinearKline_markPrice(symbol=symbol, interval=str(interval), **{'from':start}).result()[0]['result']
    return pd.DataFrame(data)


# interval has to be number of minutes and start as unix timestamp
def fetch_up_kline_indexprice_data(client, symbol, interval, start):
    data = client.LinearKline.LinearKline_indexPrice(symbol=symbol, interval=str(interval), **{'from':start}).result()[0]['result']
    return pd.DataFrame(data)

# interval has to be number of minutes and start as unix timestamp
def fetch_up_kline_premiumindexPrice_data(client, symbol, interval, start):
    data = client.LinearKline.LinearKline_premiumIndexPrice(symbol=symbol, interval=str(interval), **{'from':start}).result()[0]['result']
    return pd.DataFrame(data)


# Place Active Order
def place_up_limit_buy(client, symbol, qty, price, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.LinearOrder.LinearOrder_new(side="Buy",symbol=symbol,order_type="Limit",qty=qty,price=price,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger).result()

def place_up_limit_sell(client, symbol, qty, price, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.LinearOrder.LinearOrder_new(side="Sell",symbol=symbol,order_type="Limit",qty=qty,price=price,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger).result()

# stop loss and take profit are market orders
def place_up_limit_buy_oco(client, symbol, qty, price, tp_price, sl_price, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.LinearOrder.LinearOrder_new(side="Buy",symbol=symbol,order_type="Limit",qty=qty,price=price,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger, take_profit=tp_price, stop_loss = sl_price).result()

def place_up_limit_sell_oco(client, symbol, qty, price, tp_price, sl_price, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.LinearOrder.LinearOrder_new(side="Sell",symbol=symbol,order_type="Limit",qty=qty,price=price,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger, take_profit=tp_price, stop_loss = sl_price).result()

def place_up_market_buy(client, symbol, qty, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.LinearOrder.LinearOrder_new(side="Buy",symbol=symbol,order_type="Market",qty=qty,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger).result()

def place_up_market_sell(client, symbol, qty, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.LinearOrder.LinearOrder_new(side="Sell",symbol=symbol,order_type="Market",qty=qty,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger).result()

def place_up_market_buy_oco(client, symbol, qty, tp_price, sl_price, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.LinearOrder.LinearOrder_new(side="Buy",symbol=symbol,order_type="Market",qty=qty,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger, take_profit=tp_price, stop_loss = sl_price).result()

def place_up_market_sell_oco(client, symbol, qty, tp_price, sl_price, tif="GoodTillCancel", reduce_only=False, close_on_trigger=False):
    return client.LinearOrder.LinearOrder_new(side="Sell",symbol=symbol,order_type="Market",qty=qty,time_in_force=tif, reduce_only = reduce_only, close_on_trigger = close_on_trigger, take_profit=tp_price, stop_loss = sl_price).result()


# Get order history
def get_up_orders(client, symbol):
    return client.LinearOrder.LinearOrder_getOrders(symbol=symbol).result()[0]['result']

def cancel_up_order(client, symbol, order_id):
    return client.LinearOrder.LinearOrder_cancel(symbol=symbol, order_id=order_id).result()[0]['result']

def cancel_up_all_orders(client, symbol):
    return client.LinearOrder.LinearOrder_cancelAll(symbol=symbol).result()[0]['result']

def get_up_order_status(client, symbol, order_id):
    return client.LinearOrder.LinearOrder_query(symbol=symbol, order_id=order_id).result()[0]['result']


def amend_up_order_qty(client, symbol, order_id, new_qty):
    return client.LinearOrder.LinearOrder_replace(symbol=symbol, order_id=order_id, p_r_qty=str(new_qty)).result()[0]['result']


def amend_up_order_price(client, symbol, order_id, new_price):
    return client.LinearOrder.LinearOrder_replace(symbol=symbol, order_id=order_id, p_r_price=str(new_price)).result()[0]['result']


def place_up_limit_buy_conditional_order(client, symbol, qty, price, base_price, stop_price, tif = "GoodTillCancel", close_on_trigger = False, reduce_only=True, trigger_by="LastPrice"):
    return client.LinearConditional.LinearConditional_new(order_type="Limit",side="Buy",symbol=symbol,qty=str(qty),price=str(price), trigger_by=trigger_by,
    base_price=str(base_price),stop_px=str(stop_price),time_in_force=tif, close_on_trigger=close_on_trigger, reduce_only=reduce_only).result()


def place_up_limit_sell_conditional_order(client, symbol, qty, price, base_price, stop_price, tif = "GoodTillCancel", close_on_trigger = False, reduce_only=True,trigger_by="LastPrice"):
    return client.LinearConditional.LinearConditional_new(order_type="Limit",side="Sell",symbol=symbol,qty=str(qty),price=str(price), trigger_by=trigger_by,
    base_price=str(base_price),stop_px=str(stop_price),time_in_force=tif, close_on_trigger=close_on_trigger, reduce_only=reduce_only).result()[0]['result']

def place_up_market_buy_conditional_order(client, symbol, qty, base_price, stop_price, tif = "GoodTillCancel", close_on_trigger = False, reduce_only=True, trigger_by="LastPrice"):
    return client.LinearConditional.LinearConditional_new(order_type="Market",side="Buy",symbol=symbol,qty=str(qty), trigger_by=trigger_by,
    base_price=str(base_price),stop_px=str(stop_price),time_in_force=tif, close_on_trigger=close_on_trigger, reduce_only=reduce_only).result()


def place_up_market_sell_conditional_order(client, symbol, qty, base_price, stop_price, tif = "GoodTillCancel", close_on_trigger = False, reduce_only=True,trigger_by="LastPrice"):
    return client.LinearConditional.LinearConditional_new(order_type="Market",side="Sell",symbol=symbol,qty=str(qty), trigger_by=trigger_by,
    base_price=str(base_price),stop_px=str(stop_price),time_in_force=tif, close_on_trigger=close_on_trigger, reduce_only=reduce_only).result()[0]['result']


def get_up_untriggered_conditional_orders_history(client, symbol):
    return client.LinearConditional.LinearConditional_getOrders(symbol=symbol, stop_order_status="Untriggered").result()

# Cancel Conditional Order
def cancel_up_conditional_order(client, symbol, order_id):
    return client.LinearConditional.LinearConditional_cancel(symbol=symbol, order_id=order_id).result()[0]['result']

def cancel_up_all_conditional_orders(client, symbol):
    return client.LinearConditional.LinearConditional_cancelAll(symbol=symbol).result()[0]['result']

def get_up_conditional_order_status(client, symbol, order_id):
    return client.LinearConditional.LinearConditional_query(symbol=symbol, stop_order_id=order_id).result()[0]['result']

def amend_up_conditional_order_qty(client, symbol, order_id, new_qty):
    return client.LinearConditional.LinearConditional_replace(symbol=symbol, stop_order_id=order_id, p_r_qty=str(new_qty)).result()[0]['result']

def amend_up_conditional_order_price(client, symbol, order_id, new_price):
    return client.LinearConditional.LinearConditional_replace(symbol=symbol, stop_order_id=order_id, p_r_price=str(new_price)).result()[0]['result']

def get_up_position(client, symbol):
    return client.LinearPositions.LinearPositions_myPosition(symbol=symbol).result()[0]['result']

def change_up_margin(client, symbol, margin):
    return client.LinearPositions.LinearPositions_changeMargin(symbol=symbol, margin=str(margin)).result()[0]['result']

def position_up_trading_stop(client, symbol, tp_price, sl_price):
    return client.LinearPositions.LinearPositions_tradingStop(symbol=symbol, take_profit=str(tp_price), stop_loss=str(sl_price)).result()[0]['result']

def set_up_leverage(client, symbol, leverage):
    return client.LinearPositions.LinearPositions_saveLeverage(symbol=symbol, leverage=leverage).result()[0]['result']

def get_up_last_funding_rate(client, symbol):
    return client.LinearFunding.LinearFunding_myLastFee(symbol=symbol).result()[0]['result']

# Set Auto Add Margin
def set_up_auto_margin(client, symbol, side, auto_add_margin):
    return client.LinearPositions.LinearPositions_setAutoAddMargin(symbol=symbol, side=side, auto_add_margin=auto_add_margin).result()[0]['result']

# Cross/Isolated Margin Switch
def up_cross_isolated_switch(client, symbol, is_isolated, buy_leverage, sell_leverage):
    return client.LinearPositions.LinearPositions_switchIsolated(symbol=symbol,is_isolated=is_isolated, buy_leverage=buy_leverage, sell_leverage=sell_leverage).result()[0]['result']

# Add/Reduce Margin
def up_reduce_margin(client, symbol, side, margin):
    return client.LinearPositions.LinearPositions_changeMargin(symbol=symbol, side=side, margin=margin).result()[0]['result']

if __name__ == '__main__':
    client = bybit.bybit(test=True, api_key=config_file.accounts['bybit']['a1']['api_key'],
                         api_secret=config_file.accounts['bybit']['a1']['api_secret'])
    while True:
        try:
            # load orders
            if os.path.exists("order_details.csv"):
                orders = pd.read_csv("order_details.csv")
                for i in range(orders.shape[0]):
                    symbol = orders['symbol'].iloc[i]
                    if orders['status'].iloc[-1] == 'new':
                        # new order is a market order
                        id = place_market_margin_order(symbol, orders['side'].iloc[i], orders['amount'].iloc[i])
                        time.sleep(0.1)
                        order_details = get_order_status(symbol, id)
                        if order_details['status'] == 'closed' or order_details['status'] == 'filled':
                            orders['status'].iloc[-1] = 'active'
                            if orders['side'].iloc[i] == 'buy':
                                orders['buy_price'].iloc[i] = order_details['price']
                                orders['stop_orderid'].iloc[i] = place_stop_loss_market_order(symbol, "sell",
                                                                                              orders['stop_price'].iloc[
                                                                                                  i],
                                                                                              orders['amount'].iloc[i])
                                orders['take_profit_orderid'].iloc[i] = place_limit_margin_order(symbol, "sell", orders[
                                    'target_price'].iloc[i], orders['amount'].iloc[i])
                            elif orders['side'].iloc[i] == 'sell':
                                orders['sell_price'].iloc[i] = order_details['price']
                                orders['stop_orderid'].iloc[i] = place_stop_loss_market_order(symbol, "buy",
                                                                                              orders['stop_price'].iloc[
                                                                                                  i],
                                                                                              orders['amount'].iloc[i])
                                orders['take_profit_orderid'].iloc[i] = place_limit_margin_order(symbol, "buy", orders[
                                    'target_price'].iloc[i], orders['amount'].iloc[i])
                    elif orders['status'].iloc[-1] == 'active':
                        if orders['order_status'].iloc[-1] == 'filled' or orders['order_status'].iloc[-1] == 'closed':
                            stop_order_id = orders['stop_orderid'].iloc[i]
                            take_profit_id = orders['take_profit_orderid'].iloc[i]
                            if take_profit_id != "inactive":
                                take_profit_details = get_order_status(symbol, take_profit_id)
                                if take_profit_details['status'] == 'filled' or take_profit_details[
                                    'status'] == 'closed':
                                    # take profit is filled so cancel stop order
                                    if stop_order_id != "inactive":
                                        cancel_order(symbol, stop_order_id, 'market')
                                    # fill the selling price for buy / buying price for sell order
                                    orders['status'].iloc[i] = 'inactive'
                                    if orders['side'].iloc[i] == "buy":
                                        orders["sell_price"].iloc[i] = take_profit_details['price']
                                    elif orders['side'].iloc[i] == "sell":
                                        orders["buy_price"].iloc[i] = take_profit_details['price']
                            if stop_order_id != "inactive" and orders['status'].iloc[-1] == 'active':
                                stop_order_details = get_order_status(symbol, stop_order_id)
                                if stop_order_details['status'] == 'filled' or stop_order_details['status'] == 'closed':
                                    if take_profit_id != "inactive":
                                        cancel_order(symbol, take_profit_id, 'limit')

                                    orders['status'].iloc[i] = 'inactive'
                                    if orders['side'].iloc[i] == "buy":
                                        orders["sell_price"].iloc[i] = stop_order_details['price']
                                    elif orders['side'].iloc[i] == "sell":
                                        orders["buy_price"].iloc[i] = stop_order_details['price']

                    orders.to_csv("order_details.csv", index=False)

            time.sleep(5)
        except Exception as ex:
            print(ex)
            time.sleep(10)
            continue