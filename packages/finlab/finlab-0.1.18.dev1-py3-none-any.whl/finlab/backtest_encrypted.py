import datetime
import pandas as pd
import numpy as np
from finlab.report import Report
from finlab import data

def sim(buy, sell=None, resample=None, weight=None, trade_at_price='close', benchmark=None, fee_ratio=1.425/1000,
        tax_ratio=3/1000, name=None, stop_loss=None, stop_profit=None):

    # adjust for trading price
    if trade_at_price:
        price = data.get(f'etl:adj_{trade_at_price}')
    else:
        price = (data.get('etl:adj_close') + data.get('etl:adj_open'))/2

    # resample dates
    if isinstance(resample, str):
        dates = pd.date_range(buy.index[0], buy.index[-1], freq=resample)
        next_trading_date = min(set(pd.date_range(buy.index[0],
            datetime.datetime.now() + datetime.timedelta(days=720),
            freq=resample)) - set(dates))
    elif resample is None:
        dates = None
        next_trading_date = buy.index[-1] + datetime.timedelta(days=1)

    # calculate position using buy and sell
    positions = calculate_position(price, buy, sell, dates, weight)
    positions = sl_tp_filter(positions, stop_loss, stop_profit, trade_at_price)
    returns = calculate_capital(price, positions, fee_ratio, tax_ratio)

    # create report
    report = Report(returns, positions, benchmark, fee_ratio, tax_ratio, trade_at_price, next_trading_date)
    result = report.upload(name)

    if 'status' in result and result['status'] == 'error':
        print('Fail to upload result to server')
        print('error message', result['message'])
        return report

    try:
        url = 'https://finlab-python.github.io/strategy/?uid=' + result['uid'] + '&sid=' + result['strategy_id']
        from IPython.display import IFrame, display
        iframe = IFrame(url, width='100%', height=800)
        display(iframe)

    except Exception as e:
        pass

    return report

def rebalance_dates(freq):
    if isinstance(freq, str):
        def f(start_date, end_date):
            return pd.date_range(start_date, end_date, freq=freq)
        return f
    elif isinstance(freq, pd.Series):
        def f(start_date, end_date):
            return pd.to_datetime(freq.loc[start_date, end_date].index)
    return f

def adjust_dates_to_index(creturn, dates):

    def to_buesiness_day(d):
        if d <= creturn.index[-1]:
            i = creturn.index.get_loc(d, method='bfill')
            ret = creturn.index[i]
        else:
            ret = None#creturn.index[-1]
        return ret

    return pd.DatetimeIndex(pd.Series(dates).apply(to_buesiness_day).dropna()).drop_duplicates()

def calculate_position(price, buy, sell, resample=None, weight=None):

    '''
    signalIn and signalOut are pandas dataframe, which indicate a stock should be
    bought or not.
    '''

    if sell is not None:
        buy &= price.notna()
        sell |= price.isna()

    position = pd.DataFrame(np.nan, index=buy.index, columns=buy.columns)

    position[buy.fillna(False)] = 1
    if sell is not None:
        position[sell.fillna(False)] = 0
        position = position.ffill()
    position = position.fillna(0)

    if weight is not None:
      position *= weight.reindex_like(position).fillna(0)

    position = position.div(position.abs().sum(axis=1), axis=0).fillna(0)

    if resample is not None:
        dates = adjust_dates_to_index(price, resample)
        # position = position.reindex(price.index, method='ffill')\
        #     .reindex(dates, method='ffill')\
        #     .reindex(price.index, method='ffill').astype(float)
        position = position.reindex(dates, method='ffill').astype(float)

    # remove stock not traded
    position = position.loc[:, position.sum()!=0]

    # remove zero portfolio time period
    position = position.loc[(position.sum(axis=1) != 0).cumsum() != 0]
    return position

def calculate_capital(price, position, fee_ratio, tax_ratio):

    # shapes of price and position should be the same
    # value of price and position should not be Nan
    stocks_list = position.columns.intersection(price.columns)
    adj_close = price.loc[position.index[0]:][stocks_list]
    position = position[stocks_list].reindex(price.index, method='ffill').ffill().fillna(0)

    # forbid trading at the stock listing date
    position[adj_close.ffill().shift().isna() & adj_close.notna()] = 0

    # calculate position adjust dates
    periods = (position.diff().abs().sum(axis=1) > 0).cumsum()
    indexes = pd.Series(periods.index).groupby(periods.values).last()

    # calculate periodic returns
    selected_adj = (adj_close.shift(-2)/adj_close.shift(-1)).clip(0.9 ,1.1).groupby(periods).cumprod().fillna(1)
    selected_adj[((position == 0) | (selected_adj == 0))] = np.nan
    ret = (selected_adj.fillna(1) * position).sum(axis=1) + (1 - position.sum(axis=1))

    # calculate cost
    pdiff = position.diff()
    pdiff[pdiff > 0] *= (fee_ratio)
    pdiff[pdiff < 0] *= (fee_ratio + tax_ratio)
    cost = pdiff.abs().sum(axis=1).shift()
    cost = cost.fillna(0)

    # calculate cummulation returns
    s = (pd.Series(ret.groupby(periods).last().values, indexes).reindex(ret.index).fillna(1).shift().cumprod() * ret)

    # consider cost
    cap = ((s.shift(-1) / s).shift(3) * (1-cost)).cumprod().fillna(1)

    return cap[cap.shift(-1).fillna(1) != 1.0]


def sl_tp_filter(buy, stop_loss=None, stop_profit=None, trade_at_price='close'):
    """Add sl_sp condition in buy dataframe
    Args:
      buy(dataframe): A dataframe of buy signals.
      stop_loss(float):Stop loss benchmark,ex:0.1(10%)
      stop_profit(float):Stop profit benchmark,ex:0.1(10%)
      trade_at_price(str): Price option,close or open
    Returns:
        buy(dataframe):Intersection of signal list and stop-loss and stop-profit exit signals.

    """
    if (stop_loss is None) and (stop_profit is None):
        return buy
    adj_price = data.get(f'etl:adj_{trade_at_price}').ffill()
    buy = buy.reindex(adj_price.index, method='ffill')
    useful_columns = (buy.sum() > 0)
    buy = buy[useful_columns[useful_columns].index]
    buy_columns = buy.columns
    buy_columns = buy_columns[buy_columns.isin(adj_price.columns)]
    buy = buy[buy_columns]
    adj_price = adj_price[buy_columns]

    signal_df = (buy.shift() * adj_price).astype(float).fillna(0)
    returns = (signal_df / signal_df.shift()).replace(np.inf, 1).replace(0, np.nan).fillna(method='bfill', limit=1)
    returns = returns.cumprod()

    # get entry date
    entry_df = (buy - buy.shift()) > 0

    base_df = (returns * entry_df).replace(0, np.nan).fillna(method='ffill')
    hold_period_returns = (returns / base_df) - 1

    check_stop_loss, check_stop_profit = True, True
    if stop_loss is not None:
        check_stop_loss = (hold_period_returns > -np.abs(stop_loss))

    if stop_profit is not None:
        check_stop_profit = (hold_period_returns < np.abs(stop_profit))

    check_hold = (check_stop_loss & check_stop_profit).cumsum()
    check_hold_period = (check_hold * entry_df).replace(0, np.nan).fillna(method='ffill')
    cont_hold = check_hold - check_hold_period

    cont_values_df = buy.cumsum()
    cont_df = (cont_values_df - (cont_values_df * entry_df).replace(0, np.nan).fillna(method='ffill'))
    check_cont = cont_df - cont_hold
    sl_tp_df = check_cont < 1
    return sl_tp_df & buy
