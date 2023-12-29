from vendors.nse import NSE
from datetime import datetime as dt

class HighOI:
    def __init__(self):
        nse = NSE()
        self.df, self.underlying_value = nse.optionchain()

    def high_oi(self):
        df = self.df.sort_values('openInterest', ascending=False).head(5)
        df['time'] = str(dt.now().strftime("%H:%M"))
        return df

def get_oi_data(filename, jm, oi_data):
    data = jm.read_data(filename)
    for index, row in oi_data.iterrows():
        strikePrice = str(index)
        data.setdefault(strikePrice, []).append([row["openInterest"], row["time"]])
    jm.write_data(filename, data)
    return data