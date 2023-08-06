import os
import re
import requests
import shutil
import pickle
import datetime
import pandas as pd
from io import BytesIO
from . import login, get_token
from . import dataframe
from finlab.utils import logger

class CacheSystem():

  def __init__(self):
    self.cache = {}
    self.cache_time = {}
    self.stock_names = {}

  @staticmethod
  def expired(cache_time):
    now = datetime.datetime.now()
    pm7 = datetime.datetime(now.year, now.month, now.day, hour=19)

    if now > pm7 and cache_time < pm7:
      return True
    if now - cache_time > datetime.timedelta(hours=12):
      return True
    return False

  def exists(self, dfname):
    now = datetime.datetime.now()

    if (dfname in self.cache) and not self.expired(self.cache_time[dfname]):
      return True
    return False

  def save_cache(self, dfname, df):
    now = datetime.datetime.now()
    self.cache[dfname] = df
    self.cache_time[dfname] = now

  def cache_stock_names(self, new_stock_names):
    self.stock_names = {**self.stock_names, **new_stock_names}

  def get_cache(self, dfname):
    return self.cache[dfname]

  def get_stock_names(self):
    return self.stock_names

class FileCacheSystem():
  def __init__(self, path='./finlab_db'):
    self.path = path
    self.cache = {}
    self.cache_time = {}
    self.stock_names = None

    if not os.path.isdir(path):
      os.mkdir(path)
      pickle.dump({}, open(os.path.join(path, 'timestamp.pkl'), 'wb'))
      pickle.dump({}, open(os.path.join(path, 'stock_names.pkl'), 'wb'))
    else:
      self.cache_time = pickle.load(open(os.path.join(self.path, 'timestamp.pkl'), 'rb'))
      self.stock_names = pickle.load(open(os.path.join(self.path, 'stock_names.pkl'), 'rb'))

  def save_cache(self, dfname, df):
    file_path = os.path.join(self.path, dfname + '.pickle')
    df.to_pickle(file_path)
    timestamp = pickle.load(open(os.path.join(self.path, 'timestamp.pkl'), 'rb'))
    timestamp[dfname] = datetime.datetime.now()
    pickle.dump(timestamp, open(os.path.join(self.path, 'timestamp.pkl'), 'wb'))
    self.cache[dfname] = df
    self.cache_time[dfname] = datetime.datetime.now()

  def get_cache(self, dfname):

    if dfname in self.cache:
      return self.cache[dfname]

    file_path = os.path.join(self.path, dfname + '.pickle')
    if os.path.isfile(file_path):
      ret = pd.read_pickle(file_path)
      self.cache[dfname] = ret
      self.cache_time[dfname] = datetime.datetime.now()
      return ret
    return None

  def exists(self, dfname):
    now = datetime.datetime.now()
    if (dfname in self.cache) and not CacheSystem.expired(self.cache_time[dfname]):
      return True

    file_path = os.path.join(self.path, dfname + '.pickle')
    timestamp = pickle.load(open(os.path.join(self.path, 'timestamp.pkl'), 'rb'))
    now = datetime.datetime.now()
    ret = os.path.isfile(file_path) and dfname in timestamp and not CacheSystem.expired(timestamp[dfname])
    return ret

  def cache_stock_names(self, new_stock_names):
    stock_names = pickle.load(open(os.path.join(self.path, 'stock_names.pkl'), 'rb'))
    stock_names = {**stock_names, **new_stock_names}
    pickle.dump(stock_names, open(os.path.join(self.path, 'stock_names.pkl'), 'wb'))
    self.stock_names = stock_names

  def get_stock_names(self):
    if self.stock_names is not None:
      return self.stock_names

    stock_names = pickle.load(open(os.path.join(self.path, 'stock_names.pkl'), 'rb'))
    self.stock_names = stock_names
    return stock_names

cs = CacheSystem()
universe_stocks = set()

def set_cache_system(cs_):
  global cs
  cs = cs_

def set_universe(market='ALL', category='ALL'):
  """Set subset of stock ids when retrieve data using data.get or data.indicator

  Args:
      market (str): universe market type. ex: 'ALL', 'TSE', 'OTC', 'TSE_OTC', 'ETF'
      category (str): stock categories, can be either a string or a list. ex: '光電業', '其他', '其他電子業',
 '化學工業', '半導體', '半導體業', '塑膠工業', '存託憑證', '建材營造', '文化創意業', '橡膠工業', '水泥工業',
 '汽車工業', '油電燃氣業', '玻璃陶瓷', '生技醫療', '生技醫療業', '紡織纖維', '航運業', '觀光事業', '貿易百貨',
 '資訊服務業', '農業科技', '通信網路業', '造紙工業', '金融保險業', '金融業', '鋼鐵工業', '電器電纜', '電子商務',
 '電子工業', '電子通路業', '電子零組件', '電子零組件業', '電機機械', '電腦及週邊', '電腦及週邊設備業', '食品工業'

  Returns:
      None

  """

  categories = get('security_categories')

  market_match = pd.Series(True, categories.index)

  if market == 'ALL':
    pass
  elif market == 'TSE':
    market_match = categories.market == 'sii'
  elif market == 'OTC':
    market_match = categories.market == 'otc'
  elif market == 'TSE_OTC':
    market_match = (categories.market == 'sii') | (categories.market == 'otc')
  elif market == 'ETF':
    market_match = categories.market == 'other_securities'

  category_match = pd.Series(True, categories.index)

  if category == 'ALL':
    pass
  else:
    if isinstance(category, str):
      category = [category]

    matched_categories = set()
    all_categories = set(categories.category)
    for ca in category:
        matched_categories |= (set([c for c in all_categories if isinstance(c, str) and re.search(ca, c)]))
    category_match = categories.category.isin(matched_categories)

  global universe_stocks
  universe_stocks = set(categories.stock_id[market_match & category_match])

def get(dataset, use_cache=True):

    global universe_stocks

    # use cache if possible
    now = datetime.datetime.now()
    if cs.exists(dataset):
        ret = cs.get_cache(dataset)
        if ret.index.name != 'date':
          return ret
        if dataset.split(':')[0] not in ['price', 'monthly_revenue', 
                                     'security_lending', 'security_lending_sell', 'financial_statement'
                                    'fundamental_features']:
          return ret
        return ret if not universe_stocks else ret[ret.columns.intersection(universe_stocks)]

    api_token = get_token()

    bucket_name = 'finlab_tw_stock_item'
    if ':' in dataset:
        blob_name = dataset.replace(':', '#') + '.feather'
        file_format = 'pivot'
    else:
        blob_name = dataset + '.feather'
        file_format = 'table'

    # request for auth url
    request_args = {
        'api_token': api_token,
        'bucket_name':'finlab_tw_stock_item',
        'blob_name': dataset.replace(':', '#') + '.feather'
    }

    url = 'https://asia-east2-fdata-299302.cloudfunctions.net/auth_generate_data_url'
    auth_url = requests.get(url, request_args)
    auth_url_status_code = auth_url.status_code
    if auth_url_status_code == 401:
        logger.error("The authentication code you entered is wrong or the account does not exist."
                     "Please restart kernal to input right authentication code or register account ")
        return None

    # download and parse dataframe
    res = requests.get(auth_url.text)
    res_status_code = res.status_code
    if res_status_code == 404:
        logger.error("Your requested blob_name is not existed in finlab database."
                     "Please use right blob_name from https://ai.finlab.tw/database/")
        return None
    df = pd.read_feather(BytesIO(res.content))

    # set date as index
    if 'date' in df:
        df.set_index('date', inplace=True)

        table_name = dataset[:dataset.index(':')]
        if table_name in ['monthly_revenue', 'rotc_monthly_revnue', '財報', '財務指標']:
            close = get('price:收盤價')
            df.index = df.index.map(lambda d: d if len(close.loc[d:]) == 0 or d < close.index[0] else close.loc[d:].index[0])


        # if column is stock name
        if (df.columns.str.find(' ') != -1).all():

            # save new stock names
            new_stock_names = df.columns.str.split(' ')
            new_stock_names = dict(zip(new_stock_names.str[0], new_stock_names.str[1]))
            cs.cache_stock_names(new_stock_names)

            # remove stock names
            df.columns = df.columns.str.split(' ').str[0]

            # combine same stock history according to sid
            df = df.transpose().groupby(level=0).mean().transpose()


        df = dataframe.FinlabDataFrame(df)

    # save cache
    if use_cache:
        cs.save_cache(dataset, df)

    if df.index.name != 'date':
        return df
    
    if dataset.split(':')[0] not in ['price', 'monthly_revenue', 
                                 'security_lending', 'security_lending_sell', 'financial_statement'
                                'fundamental_features']:
      return df

    return df if not universe_stocks else df[df.columns.intersection(universe_stocks)]

def indicator(indname, adjust_price=False, resample='D', **kwargs):

    from talib import abstract

    func = getattr(abstract, indname)

    isSeries = True if len(func.output_names) == 1 else False
    names = func.output_names
    if isSeries:
        dic = {}
    else:
        dics = {n:{} for n in names}

    if adjust_price:
        close  = get('etl:adj_close')
        open_  = get('etl:adj_open')
        high   = get('etl:adj_high')
        low    = get('etl:adj_low')
        volume = get('price:成交股數')
    else:
        close  = get('price:收盤價')
        open_  = get('price:開盤價')
        high   = get('price:最高價')
        low    = get('price:最低價')
        volume = get('price:成交股數')

    if resample.upper() != 'D':
        close = close.resample(resample).last()
        open_ = open_.resample(resample).first()
        high = high.resample(resample).max()
        low = low.resample(resample).min()
        volume = volume.resample(resample).sum()

    for key in close.columns:
        try:
            s = func({'open':open_[key].ffill(),
                           'high':high[key].ffill(),
                           'low':low[key].ffill(),
                           'close':close[key].ffill(),
                           'volume':volume[key].ffill()}, **kwargs)
        except Exception as e:
            if "inputs are all NaN" != str(e):
                print('Warrning occur during calculating stock '+key+':',e)
                print('The indicator values are set to NaN.')
            if isSeries:
                s = pd.Series(index=close[key].index)
            else:
                s = pd.DataFrame(index=close[key].index, columns=dics.keys())

        if isSeries:
            dic[key] = s
        else:
            for colname, si in zip(names, s):
                dics[colname][key] = si

    if isSeries:
        ret = pd.DataFrame(dic, index=close.index)
        ret = ret.apply(lambda s:pd.to_numeric(s, errors='coerce'))
    else:
        newdic = {}
        for key, dic in dics.items():
            newdic[key] = pd.DataFrame(dic, close.index)
        ret = [newdic[n] for n in names]#pd.Panel(newdic)
        ret = [d.apply(lambda s:pd.to_numeric(s, errors='coerce')) for d in ret]

    return dataframe.FinlabDataFrame(ret)
