class Config:
    def __init__(self, open, high, low, close) -> None:
        self.body: float = abs(open - close)
        self.doubleBody: float = self.body * 2

        self.redTopTail: float = high - open
        self.redBottomTail: float = close - low

        self.doubleRedTopTail: float = self.redTopTail * 2
        self.doubleRedBottomTail: float = self.redBottomTail * 2

        self.greenTopTail: float = high - close
        self.greenBottomTail: float = open - low

        self.doubleGreenTopTail: float = self.greenTopTail * 2
        self.doubleGreenBottomTail: float = self.greenBottomTail * 2

    def deltaFinder(self):
        ### Topping Tail
        # Delta Double Green Bottom Tail ÷ Green Top Tail
        self.deltaGBGT: float = self.doubleGreenBottomTail / self.greenTopTail
        # Delta Green Double Body ÷ Green Top Tail
        self.deltaGTGT: float = self.doubleBody / self.greenTopTail

        # Delta Double Red Bottom Tail ÷ Red Top Tail
        self.deltaRBRT: float = self.doubleRedBottomTail / self.redTopTail
        # Delta Red Double Body ÷ Red Top Tail
        self.deltaRTRT: float = self.doubleBody / self.redTopTail

        ### Bottoming Tail
        # Delta Double Green Top Tail ÷ Green Bottom Tail
        self.deltaGTGB: float = self.doubleGreenTopTail / self.greenBottomTail
        # Delta Green Double Body ÷ Green Bottom Tail
        self.deltaGBGB: float = self.doubleBody / self.greenBottomTail

        # Delta Double Red Top Tail ÷ Red Bottom Tail
        self.deltaRTRB: float = self.doubleRedTopTail / self.redBottomTail
        # Delta Red Double Body ÷ Red Bottom Tail
        self.deltaRBRB: float = self.doubleBody / self.redBottomTail
