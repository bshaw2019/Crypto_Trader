import ccxt
import time
import datetime
import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import threading
import dataset
from collections import deque


class CryptoDataGrabber(object):

    def __init__(self):
        """"""
        self.exchange = ccxt.poloniex()
        self.exchange.load_markets()
        self.delay_seconds = self.exchange.rateLimit / 1000
        self.symbols = self.exchange.markets
        self.timeframe = '1d'
        self.db_url = 'sqlite:///databases/market_prices.db'
        self.deques = dict()
        self.ohlcv = dict()
        self.database = dataset.connect(self.db_url)
        for symbol in self.symbols:
            if self.exchange.has['fetchOHLCV']:
                print('Obtaining OHLCV data')
                data = self.exchange.fetch_ohlcv(symbol, self.timeframe)
                data = list(zip(*data))
                data[0] = [datetime.datetime.fromtimestamp(ms / 1000)
                           for ms in data[0]]
                self.ohlcv[symbol] = data
                time.sleep(self.delay_seconds)
            else:
                print('No OHLCV data available')
            self.deques[symbol] = deque()
            if len(self.database[symbol]):
                for e in self.database[symbol]:
                    entry = (e['bid'], e['ask'], e['spread'], e['time'])
                    self.deques[symbol].append(entry)
        del self.database
        self.thread = threading.Thread(target=self.__update)
        self.thread.daemon = True
        self.thread.start()

    def get_symbols(self):
        """"""
        return self.deques.keys()

    def get_prices(self, symbol):
        """"""
        return self.deques[symbol]

    def get_ohlcv(self, symbol):
        """"""
        data = self.ohlcv[symbol]
        return data[0], data[1], data[2], data[3], data[4], data[5]

    def __update(self):
        """
        https://github.com/ccxt-dev/ccxt/wiki/Manual#market-price
        """
        self.database = dataset.connect(self.db_url)
        while True:
            for symbol in self.symbols:

                start_time = time.clock()
                orders = self.exchange.fetch_order_book(symbol)
                bid = orders['bids'][0][0] if len(orders['bids']) > 0 else None
                ask = orders['asks'][0][0] if len(orders['asks']) > 0 else None
                spread = (ask - bid) if (bid and ask) else None
                dtime = datetime.datetime.now()
                self.deques[symbol].append((bid, ask, spread, dtime))
                self.database.begin()
                try:
                    self.database[symbol].insert({
                        'ask': ask,
                        'bid': bid,
                        'spread': spread,
                        'time': dtime
                    })
                    self.database.commit()
                except:
                    self.database.rollback()

                time.sleep(self.delay_seconds - (time.clock() - start_time))


data = CryptoDataGrabber()

selected_dropdown_value = 'ETH/BTC'

app = dash.Dash()
app.layout = html.Div([
    html.Div([
        html.H1('Poloniex Nerd', id='h1_title'),
        dcc.Dropdown(
            id='symbol-dropdown',
            options=[{'label': key, 'value': key}
                     for key in data.get_symbols()],
            value=selected_dropdown_value
        ),
        html.Div([
            dcc.Graph(
                id='ohlc',
                config={
                    'displayModeBar': False
                }
            ),
        ], className="row"),
        html.Div([
            dcc.Graph(
                id='v',
                config={
                    'displayModeBar': False
                }
            ),
        ], className="row"),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='market-prices-graph',
                    config={
                        'displayModeBar': False
                    }
                ),
                dcc.Graph(
                    id='spread-graph',
                    config={
                        'displayModeBar': False
                    }
                ),
            ], className="eight columns"),
            html.Div([
                dcc.Graph(
                    id='market-prices-hist',
                    config={
                        'displayModeBar': False
                    }
                ),
                dcc.Graph(
                    id='spread-hist',
                    config={
                        'displayModeBar': False
                    }
                ),
            ], className="four columns")
        ], className="row"),
        dcc.Interval(id='graph-speed-update', interval=2000),
    ], className="row")
])
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


@app.callback(Output('h1_title', 'children'),
              [Input('symbol-dropdown', 'value')])
def change_plot(value):
    global selected_dropdown_value
    selected_dropdown_value = value
    return 'Market Prices ' + str(value)


@app.callback(Output('ohlc', 'figure'),
              [Input('symbol-dropdown', 'value')])
def plot_olhc(value):
    global data
    dates, open_data, high_data, low_data, close_data, _ \
        = data.get_ohlcv(value)
    return {
        'data': [go.Ohlc(x=dates,
                         open=open_data,
                         high=high_data,
                         low=low_data,
                         close=close_data)],
        'layout': dict(title="OHLC")
    }


@app.callback(Output('v', 'figure'),
              [Input('symbol-dropdown', 'value')])
def plot_v(value):
    global data
    dates, _, _, _, _, volume = data.get_ohlcv(value)
    return {
        'data': [go.Bar(x=dates,
                        y=volume)],
        'layout': dict(title="Volume")
    }


@app.callback(Output('market-prices-graph', 'figure'),
              events=[Event('graph-speed-update', 'interval')])
def update_market_prices():
    global selected_dropdown_value
    global data
    prices = data.get_prices(selected_dropdown_value)
    prices = [list(p) for p in zip(*prices)]
    if len(prices) > 0:
        traces = []
        x = list(prices[3])
        for i, key in enumerate(['bid', 'ask']):
            trace = go.Scatter(x=x,
                               y=prices[i],
                               name=key,
                               opacity=0.8)
            traces.append(trace)
        return {
            'data': traces,
            'layout': dict(title="Market Prices")
        }


@app.callback(Output('market-prices-hist', 'figure'),
              events=[Event('graph-speed-update', 'interval')])
def update_market_prices_hist():
    global selected_dropdown_value
    global data
    prices = data.get_prices(selected_dropdown_value)
    prices = [list(p) for p in zip(*prices)]
    if len(prices) > 0:
        traces = []
        for i, key in enumerate(['bid', 'ask']):
            trace = go.Histogram(x=prices[i][-200:],
                                 name=key,
                                 opacity=0.8)
            traces.append(trace)
        return {
            'data': traces,
            'layout': dict(title="Market Prices Histogram (200 Most Recent)")
        }


@app.callback(Output('spread-graph', 'figure'),
              events=[Event('graph-speed-update', 'interval')])
def update_spread():
    global selected_dropdown_value
    global data
    prices = data.get_prices(selected_dropdown_value)
    prices = [list(p) for p in zip(*prices)]
    if len(prices) > 0:
        traces = []
        trace = go.Scatter(x=list(prices[3]),
                           y=list(prices[2]),
                           name='spread',
                           line=dict(color='rgb(114, 186, 59)'),
                           fill='tozeroy',
                           fillcolor='rgba(114, 186, 59, 0.5)',
                           mode='none')
        traces.append(trace)

        return {
            'data': traces,
            'layout': dict(title="Spread")
        }


@app.callback(Output('spread-hist', 'figure'),
              events=[Event('graph-speed-update', 'interval')])
def update_spread_hist():
    global selected_dropdown_value
    global data
    prices = data.get_prices(selected_dropdown_value)
    prices = [list(p) for p in zip(*prices)]
    if len(prices) > 0:
        traces = []
        trace = go.Histogram(x=list(prices[2][-200:]),
                             name='spread',
                             marker=dict(color='rgba(114, 186, 59, 0.5)'))
        traces.append(trace)

        return {
            'data': traces,
            'layout': dict(title="Spread Histogram (200 Most Recent)")
        }


if __name__ == '__main__':
    app.run_server()