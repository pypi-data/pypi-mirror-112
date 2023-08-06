from finlab.online.sinopac_account import SinopacAccount
from finlab.online.enums import *
import pandas as pd

class OrderExecutor():

  def __init__(self, target_position:dict, account=None):
    account = account or SinopacAccount()
    self.account = account
    self.target_position = target_position

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
