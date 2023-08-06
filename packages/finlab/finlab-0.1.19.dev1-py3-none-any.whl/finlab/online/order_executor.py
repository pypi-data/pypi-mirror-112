from finlab.online.sinopac_account import SinopacAccount
from finlab.online.utils import greedy_allocation
from finlab.online.enums import *
import pandas as pd
import requests
import time

class OrderExecutor():

  def __init__(self, target_position:dict, account=None):
    account = account or SinopacAccount()
    self.account = account
    self.target_position = target_position
    
  @classmethod
  def from_report(cls, report, money, account=None):
    
    report_position = report.position.iloc[-1]
    report_position = report_position[report_position != 0].to_dict()

    return cls.from_weights(report_position, money)

  @classmethod
  def from_weights(cls, weights, money, account=None):

    account = account or SinopacAccount()
    time.sleep(10)
    stocks = account.get_stocks(list(weights.keys()))
    stock_price = {sid: s.close * 1000 for sid, s in stocks.items()}

    allocation = greedy_allocation(weights, stock_price, money)
    return cls(allocation[0], account)

  def show_alerting_stocks(self):

    new_orders = self._calculate_new_orders()

    contracts = [self.account.api.Contracts.Stocks.get(code) for code in new_orders.keys()]
    market_data = self.account.api.snapshots([c for c in contracts if c is not None])
    market_data = {snapshot.code: snapshot for snapshot in market_data}

    res = requests.get('https://www.sinotrade.com.tw/Stock/Stock_3_8_3')
    dfs = pd.read_html(res.text)
    credit_sids = dfs[0][dfs[0]['股票代碼'].isin(list(new_orders.keys()))]['股票代碼']

    res = requests.get('https://www.sinotrade.com.tw/Stock/Stock_3_8_1')
    dfs = pd.read_html(res.text)
    credit_sids = credit_sids.append(dfs[0][dfs[0]['股票代碼'].isin(list(new_orders.keys()))]['股票代碼'].astype(str))
    credit_sids.name = None

    for sid in list(credit_sids.values):
      total_amount = new_orders[sid]*market_data[sid].close*1000
      if new_orders[sid] > 0:
        print(f"買入 {sid} {new_orders[sid]:>5} 張 - 總價約 {total_amount:>15.2f}")
      else:
        print(f"賣出 {sid} {new_orders[sid]:>5} 張 - 總價約 {total_amount:>15.2f}")
  def _calculate_new_orders(self, verbose=False):
    """create new orders in order to rebalance the old positions to new positions

        Parameters:
        target_position (dict): a dictionary with stock_id and the number of lot

        Returns:
        dict: new orders which update old positions.
    """
    # get present positions

    present_positions = self.account.get_position()
    target_positions = pd.Series(self.target_position).astype(int).to_dict()

    # calculate the difference between present position and target position
    all_codes = set(list(target_positions.keys()) + list(present_positions.keys()))
    new_orders = (pd.Series(target_positions).reindex(all_codes).fillna(0) -
                    pd.Series(present_positions).reindex(all_codes).fillna(0)).astype(int)
    new_orders = new_orders[new_orders!=0].to_dict()

    if verbose:
      print('Present positions:')
      print(pd.Series(present_positions))
      print('------------------')
      print('Target positions:')
      print(pd.Series(target_positions))
      print('------------------')
      # print the new orders
      print('new orders to rebalance:')
      if new_orders:
        print(pd.Series(new_orders))
      else:
        print('None')
      print('------------------')

    return {n:v for n,v in new_orders.items() if v != 0}

  def cancel_orders(self):
    orders = self.account.get_orders()
    for oid, o in orders.items():
      if o.status == OrderStatus.NEW or o.status == OrderStatus.PARTIALLY_FILLED:
        self.account.cancel_order(o.order_id)

  def create_orders(self, schedule=1, force=False):

    assert 0 <= schedule <= 1

    self.cancel_orders()
    orders = self._calculate_new_orders()
    orders = {stock_id: int(quantity * schedule) for stock_id, quantity in orders.items()}
    orders = {stock_id: quantity for stock_id, quantity in orders.items() if quantity != 0}
    stocks = self.account.get_stocks(list(orders.keys()))

    # make orders
    for code, quantity in orders.items():
      action = Action.BUY if quantity > 0 else Action.SELL
      price = stocks[code].close
      print('execute', action, code, 'X', abs(quantity), '@', price)
      self.account.create_order(action=action,
                                stock_id=code,
                                quantity=abs(quantity),
                                price=price, force=force)

  def update_order_price(self):
    orders = self.account.get_orders()
    sids = set([o.stock_id for i, o in orders.items()])
    stocks = self.account.get_stocks(sids)

    for i, o in orders.items():
      if o.status == OrderStatus.NEW or o.status == OrderStatus.PARTIALLY_FILLED:
        self.account.update_order(i, price=stocks[o.stock_id].close)

  def schedule(self, time_period=10, open_schedule=0, close_schedule=0):

    now = datetime.datetime.now()

    # market open time
    am0900 = now.replace(hour=8, minute=59, second=0, microsecond=0)

    # market close time
    pm1430 = now.replace(hour=14, minute=29, second=0, microsecond=0)

    # order timings
    am0905 = now.replace(hour=9, minute=5, second=0, microsecond=0)
    pm1428 = now.replace(hour=14, minute=28, second=0, microsecond=0)
    internal_timings = pd.date_range(am0905, pm1425, freq=str(time_period) + 'T')

    prev_time = datetime.datetime.now()

    first_limit_order = True

    while True:
      prev_time = now
      now = datetime.datetime.now()

      # place force orders at market open
      if prev_time < am0900 < now:
        self.create_orders(schedule=open_schedule, force=True)

      # place limit orders during 9:00 ~ 14:30
      if ((internal_timings > prev_time) & (internal_timings < now)).any():
        if first_limit_order:
          self.create_orders(schedule=1, force=False)
          first_limit_order = False
        else:
          self.update_orders()

      # place force orders at market close
      if prev_time < pm1428 < now:
        self.create_orders(schedule=close_schedule, force=True)
        break

      time.sleep(20)
