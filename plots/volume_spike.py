from vendors.nse import NSE

class VolumeSpike:
    def __init__(self) -> None:
        nse = NSE()
        self.df = nse.equity()

    def volume_spike(self):
        df = self.df.sort_values(by='totalTradedVolume', ascending=False)
        return df

def get_volume_data(filename, jm, volume_data):
    data = jm.read_data(filename)
    for index, row in volume_data.iterrows():
        strikePrice = str(index)
        data.setdefault(strikePrice, []).append(row['totalTradedVolume'])
    jm.write_data(filename, data)
    return data