class CandleInterface:
    open: float
    high: float
    low: float
    close: float

    def isRed():
        ...
    def isGreen():
        ...
    def isDoji():
        ...