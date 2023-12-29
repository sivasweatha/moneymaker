from vendors.request_methods import RequestMethods
from vendors.nse_formatter import NSEFormatter

class NSE:
    def __init__(self) -> None:
        self.url_oc = "https://www.nseindia.com/option-chain"
        self.rm = RequestMethods(self.url_oc)
        self.formatter = NSEFormatter()

    def optionchain(self, index= "NIFTY"):
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={index}"
        data = self.rm.get_data(url)
        return self.formatter.option_chain(data)

    def equity(self, index="NIFTY 50"):
        url = f"https://www.nseindia.com/api/equity-stockIndices?index={index}"
        data = self.rm.get_data(url)
        return self.formatter.equity(data, index)