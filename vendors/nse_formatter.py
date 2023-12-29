import json
import pandas as pd

class NSEFormatter:
    def __init__(self) -> None:
        pass

    def option_chain(self, data):
        try:
            data = json.loads(data)["records"]["data"]
            df = pd.DataFrame.from_dict(data)
            pe = pd.DataFrame(df["PE"].to_dict()).T
            pe['strikePrice'] = pe['strikePrice'].astype(str).apply(lambda x: x + 'PE')
            ce = pd.DataFrame(df["CE"].to_dict()).T
            ce['strikePrice'] = ce['strikePrice'].astype(str).apply(lambda x: x + 'CE')
            df = pd.concat([pe, ce], axis=0, ignore_index=True).dropna()
            self.value = df.loc[0]['underlyingValue']
            df.index = df['strikePrice']
            df = df.drop(
                ["strikePrice",
                "underlyingValue",
                "underlying",
                "identifier",
                "pchangeinOpenInterest",
                "impliedVolatility",
                "pChange",
                "totalBuyQuantity",
                "totalSellQuantity",
                "bidQty",
                "bidprice",
                "askQty",
                "askPrice"],
                axis="columns")
            return df, self.value
        except (json.JSONDecodeError, KeyError) as e:
            return self.handle_data_error(e)

    def equity(self, data, stock):
        try:
            data = json.loads(data)["data"]
            df = pd.json_normalize(data)
            df.index = df['symbol']
            df = df[df['symbol'] != stock]
            df = df.drop(
                ['symbol',
                'priority',
                'identifier',
                'series',
                'pChange',
                'lastUpdateTime',
                'yearHigh',
                'ffmc',
                'yearLow',
                'nearWKH',
                'nearWKL',
                'perChange365d',
                'date365dAgo',
                'chart365dPath',
                'date30dAgo',
                'perChange30d',
                'chart30dPath',
                'chartTodayPath',
                'meta.symbol',
                'meta.companyName',
                'meta.industry',
                'meta.activeSeries',
                'meta.debtSeries',
                'meta.tempSuspendedSeries',
                'meta.isFNOSec',
                'meta.isCASec',
                'meta.isSLBSec',
                'meta.isDebtSec',
                'meta.isSuspended',
                'meta.isETFSec',
                'meta.isDelisted',
                'meta.isin',
                'meta.quotepreopenstatus.equityTime',
                'meta.quotepreopenstatus.preOpenTime',
                'meta.quotepreopenstatus.QuotePreOpenFlag'],
                axis="columns")
            return df
        except (json.JSONDecodeError, KeyError) as e:
            return self.handle_data_error(e)

    def handle_data_error(self, e):
        print(f"Error formatting data: {e}")
        return None