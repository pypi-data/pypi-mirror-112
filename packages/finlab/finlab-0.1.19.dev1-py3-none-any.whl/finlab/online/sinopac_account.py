from abc import ABC, abstractmethod
import pandas as pd
import shioaji as sj
import datetime
import numbers
import os

from finlab.online.base_account import Account, Stock, Order
from finlab.online.enums import *

class SinopacAccount(Account):
  def __init__(self, account=None, password=None, certificate_path=None):

    account = account or os.environ.get('SHIOAJI_ACCOUNT')
    password = password or os.environ.get('SHIOAJI_PASSWORD')
    certificate_path = os.environ.get('SHIOAJI_CERT_PATH')

    if account is None or password is None or certificate_path is None:
      self.login()
      account = account or os.environ.get('SHIOAJI_ACCOUNT')
      password = password or os.environ.get('SHIOAJI_PASSWORD')
      certificate_path = os.environ.get('SHIOAJI_CERT_PATH')

    self.api = sj.Shioaji()
    self.accounts = self.api.login(account, password)

    if certificate_path:
      self.api.activate_ca(
        ca_path=certificate_path,
        ca_passwd=account,
        person_id=account,
      )

    self.trades = {}
    
  @staticmethod
  def login():
    account = input('Account name not found, please enter account name:\n')
    password = input('Enter an account password:\n')
    cert_path = input('Enter certificate path:\n')

    os.environ['SHIOAJI_ACCOUNT'] = account
    os.environ['SHIOAJI_PASSWORD'] = password
    os.environ['SHIOAJI_CERT_PATH'] = cert_path

  def create_order(self, action, stock_id, quantity, price=None, force=False):

    contract = self.api.Contracts.Stocks.get(stock_id)
    print('quantity', quantity)

    assert quantity > 0
    assert contract is not None

    if price == None:
      price = self.api.snapshots([contract])[0].close

    if force:
      if action == Action.BUY:
        price = contract.limit_up
      elif action == Action.SELL:
        price = contract.limit_down

    if action == Action.BUY:
      action = 'Buy'
    elif action == Action.SELL:
      action = 'Sell'

    order = self.api.Order(price=price,
      quantity=quantity,
      action=action,
      price_type="LMT",
      order_type="ROD",
      order_lot="Common",
      account=self.api.stock_account
    )
    trade = self.api.place_order(contract, order)

    self.trades[trade.status.id] = trade
    return trade.status.id
  def update_trades(self):
    self.api.update_status(self.api.stock_account)
    self.trades = {t.status.id: t for t in self.api.list_trades()}

  def update_order(self, order_id, **argv):
    trade = self.trades[order_id]
    self.api.update_order(trade, **argv)

  def cancel_order(self, order_id):
    self.update_trades()
    self.api.cancel_order(self.trades[order_id])

  def get_position(self):
    position = self.api.list_positions(self.api.stock_account)
    return {p.code: p.quantity for p in position}

  def get_orders(self):
    self.update_trades()
    return {t.status.id: Order.from_shioaji(t) for name, t in self.trades.items()}

  def get_stocks(self, stock_ids):
    contracts = [self.api.Contracts.Stocks.get(s) for s in stock_ids]
    snapshots = self.api.snapshots(contracts)
    return {s.code:Stock.from_shioaji(s) for s in snapshots}

  def get_total_balance(self):
    # get bank balance
    bank_balance = self.api.account_balance()[0].acc_balance

    # get settlements
    settlements = self.api.list_settlements(oe.account.api.stock_account)
    settlements = settlements[0].t_money + settlements[0].t1_money + settlements[0].t2_money

    # get position balance
    position = self.get_position()
    stocks = self.get_stocks(position.keys())
    account_balance = sum([qty * stocks[sid].close * 1000 for sid, qty in position.items()])
    return bank_balance + settlements + account_balance

