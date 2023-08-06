from datetime import date, datetime
import pandas as pd
import numpy as np
import requests
import math
import json
import ffn
import os
from . import cells
from . import get_token
from . import data

class Report(object):

    def __init__(self, creturn, position, fee_ratio, tax_ratio, trade_at, next_trading_date):
        self.creturn = creturn
        self.position = position
        self.benchmark = None
        self.fee_ratio = fee_ratio
        self.tax_ratio = tax_ratio
        self.trade_at = trade_at
        self.update_date = position.index[-1]

        position_changed = position.diff().abs().sum(axis=1)
        self.last_trading_date = position_changed[position_changed != 0].index[-1]
        self.next_trading_date = next_trading_date

    def display(self):

        if self.benchmark is not None:
            performance = pd.DataFrame({
              'strategy': self.creturn,
              'benchmark': self.benchmark.dropna()}).dropna().rebase()
        else:
            performance = pd.DataFrame({
              'strategy': self.creturn}).dropna().rebase()
        try:
            fig = self.create_performance_figure(performance, (self.position!=0).sum(axis=1))
            p = self.position.iloc[-1]

            from IPython.display import display
            display(fig)
            display(p[p!=0])
            display(self.position.index[-1])
            return fig
        except:
            pass

    @staticmethod
    def create_performance_figure(performance_detail, nstocks):

        from plotly.subplots import make_subplots
        import plotly.graph_objs as go
        # plot performance
        def diff(s, period):
            return (s / s.shift(period)-1)

        drawdowns = performance_detail.to_drawdown_series()

        fig = go.Figure(make_subplots(rows=4, cols=1, shared_xaxes=True, row_heights=[2,1,1,1]))
        fig.add_scatter(x=performance_detail.index, y=performance_detail.strategy/100-1, name='strategy', row=1, col=1, legendgroup='performnace', fill='tozeroy')
        fig.add_scatter(x=drawdowns.index, y=drawdowns.strategy, name='strategy - drawdown', row=2, col=1, legendgroup='drawdown', fill='tozeroy')
        fig.add_scatter(x=performance_detail.index, y=diff(performance_detail.strategy, 20),
                        fill='tozeroy', name='strategy - month rolling return',
                        row=3, col=1, legendgroup='rolling performance',)

        if 'benchmark' in performance_detail.columns:
            fig.add_scatter(x=performance_detail.index, y=performance_detail.benchmark/100-1, name='benchmark', row=1, col=1, legendgroup='performance', line={'color': 'gray'})
            fig.add_scatter(x=drawdowns.index, y=drawdowns.benchmark, name='benchmark - drawdown', row=2, col=1, legendgroup='drawdown', line={'color': 'gray'})
            fig.add_scatter(x=performance_detail.index, y=diff(performance_detail.benchmark, 20),
                            fill='tozeroy', name='benchmark - month rolling return',
                            row=3, col=1, legendgroup='rolling performance', line={'color': 'rgba(0,0,0,0.2)'})


        fig.add_scatter(x=nstocks.index, y=nstocks, row=4, col=1, name='nstocks', fill='tozeroy')
        fig.update_layout(legend={'bgcolor': 'rgba(0,0,0,0)'},
            margin=dict(l=60, r=20, t=40, b=20),
            height=600,
            width=800,
            xaxis4=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                              label="1m",
                              step="month",
                              stepmode="backward"),
                        dict(count=6,
                              label="6m",
                              step="month",
                              stepmode="backward"),
                        dict(count=1,
                              label="YTD",
                              step="year",
                              stepmode="todate"),
                        dict(count=1,
                              label="1y",
                              step="year",
                              stepmode="backward"),
                        dict(step="all")
                    ]),
                    x=0,
                    y=1,
                ),
                rangeslider={'visible': True, 'thickness': 0.1},
                type="date",
            ),
            yaxis={'tickformat':',.0%',},
            yaxis2={'tickformat':',.0%',},
            yaxis3={'tickformat':',.0%',},
          )
        return fig

    def upload(self, name=None):

        name = os.environ.get('FINLAB_FORCED_STRATEGY_NAME', None) or name or '未命名'

        # calculate statistic values
        s = self.creturn.calc_stats()
        s.set_riskfree_rate(0.02)

        # drawdown_detail
        drawdown_details = s.drawdown_details.sort_values('Length').tail(5)
        drawdown_details['Start'] = drawdown_details['Start'].astype(str).str.split(' ').str[0]
        drawdown_details['End'] = drawdown_details['End'].astype(str).str.split(' ').str[0]
        drawdown_details = drawdown_details.set_index('Start').to_dict('index')

        # stats
        stats = s.stats.to_dict()
        stats['start'] = stats['start'].strftime('%Y-%m-%d')
        stats['end'] = stats['end'].strftime('%Y-%m-%d')

        # creturn
        return_ = self.creturn.ffill().dropna().rebase()
        creturn = {'time':return_.index.astype(str).to_list(), 'value':return_.values.tolist()}

        # benchmark
        benchmark = (data.get('benchmark_return:發行量加權股價報酬指數')\
                .squeeze().dropna().reindex(self.creturn.index, method='ffill')\
                .ffill().rebase()).values.tolist()

        # return table
        return_table = s.return_table.transpose().to_dict()

        # ndays return
        ndays_return = {d:self.get_ndays_return(return_, d) for d in [1, 5, 10, 20, 60]}

        d = {
            # backtest info
            'drawdown_details': drawdown_details,
            'stats': stats,
            'returns': creturn,
            'benchmark': benchmark,
            'ndays_return': ndays_return,
            'return_table': return_table,
            'fee_ratio': self.fee_ratio,
            'tax_ratio': self.tax_ratio,
            'trade_at': self.trade_at,

            # dates
            'update_date': self.update_date.strftime('%Y-%m-%d'),
            'last_trading_date': self.last_trading_date.strftime('%Y-%m-%d'),
            'next_trading_date': self.next_trading_date.strftime('%Y-%m-%d'),

            # key data
            'position': self.position_info(self.position),

            # public
            'public_performance': False,
            'public_code': False,
            'public_position': False,
            }

        payload = {'data': json.dumps(d),
            'api_token': get_token(),
            'collection': 'strategies',
            'document_id': name}

        res = requests.post('https://asia-east2-fdata-299302.cloudfunctions.net/write_database', data=payload).text

        try:
            return json.loads(res)
        except:
            return {'status':'error', 'message': res}

    def position_info(self, position):

        # calculate lastest position changes
        diff = position.diff().abs().sum(axis=1)
        position_change_dates = diff.index[diff != 0]
        present_date = position_change_dates[-1]
        previous_date = position_change_dates[-2]
        p1 = position.loc[previous_date]
        p2 = position.loc[present_date]

        # record position changes
        status = pd.Series('持有', p2.index)
        status[(p1 == 0) & (p2 != 0)] = '買進'
        status[(p1 != 0) & (p2 == 0)] = '賣出'
        status = status[(p1 != 0) | (p2 != 0)].sort_values()

        # record present position weight
        weights = p2[status.index]

        # find entry dates
        entry_dates = {}
        for sid in status.index:
            has_position = (position[sid] != 0)
            first_day_enter_position = has_position & (~has_position.shift(fill_value=False))
            first_day_enter_position = first_day_enter_position[first_day_enter_position].index[-1]
            entry_dates[sid] = first_day_enter_position.strftime('%Y-%m-%d')

        # find exit dates
        exit_dates = {}
        for sid, sstatus in status.items():
            if sstatus == '賣出':
                exit_dates[sid] = present_date.strftime('%Y-%m-%d')
            else:
                exit_dates[sid] = None

        # find return
        creturn = {}
        for sid in status.index:
            creturn[sid] = self.get_return(self.trade_at, sid, entry_dates[sid], exit_dates[sid])

        # data formation
        df = pd.DataFrame({'status': status, 'weight': weights, 'entry_date': entry_dates, 'exit_date': exit_dates, 'return': creturn})
        df.sort_values(['status', 'entry_date'], inplace=True)
        df['entry_date'] = df['entry_date'].fillna('')
        df['exit_date'] = df['exit_date'].fillna('')
        stock_names = data.cs.get_stock_names()
        df.index = df.index + df.index.map(lambda sid: stock_names.get(sid, ''))

        ret = df.to_dict('index')
        ret['update_date'] = self.update_date.strftime('%Y-%m-%d')
        ret['next_trading_date'] = self.next_trading_date.strftime('%Y-%m-%d')
        ret['trade_at'] = self.trade_at
        return ret

    @staticmethod
    def get_ndays_return(creturn, n):
        last_date_eq = creturn.iloc[-1]
        ref_date_eq = creturn.iloc[-1-n]
        return last_date_eq / ref_date_eq - 1

    @staticmethod
    def get_return(trade_at, stock_id, sdate, edate=None):

        price = data.get(f'etl:adj_{trade_at}')

        sdate = pd.to_datetime(sdate)
        edate = pd.to_datetime(edate)
        if stock_id not in price.columns:
            return 0

        if sdate >= price.index[-1]:
            return 0

        price = price[stock_id]

        # get start index
        if sdate in price.index:
            sdate = price.loc[sdate:].index[1]
        else:
            sdate = price.loc[sdate:].index[0]

        assert sdate in price.index
        sindex = price.index.get_loc(sdate)

        # get end index
        if edate is None or edate >= price.index[-1]:
            eindex = len(price) - 1
        elif edate in price.index:
            eindex = price.index.get_loc(edate) + 1
        else:
            eindex = price.index.loc[edate:].iloc[0]

        evalue = np.nan
        while math.isnan(evalue) and eindex > -1:
            evalue = price.iloc[eindex]
            eindex -= 1

        svalue = np.nan
        while math.isnan(svalue) and sindex < len(price):
            svalue = price.iloc[sindex]
            sindex += 1

        return evalue / svalue - 1 # price[stock_id].ffill().iloc[eindex] / price[stock_id].bfill().iloc[sindex] - 1



