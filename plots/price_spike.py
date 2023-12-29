from vendors.nse import NSE

class PriceSpike:
    def __init__(self) -> None:
        nse = NSE()
        self.df = nse.equity()

    def price_spike(self):
        df = self.df.sort_values(by='change', ascending=False)
        return df

def get_price_data(filename, jm, price_data):
    data = jm.read_data(filename)
    for index, row in price_data.iterrows():
        strikePrice = str(index)
        data.setdefault(strikePrice, []).append(row['change'])
    jm.write_data(filename, data)
    return data