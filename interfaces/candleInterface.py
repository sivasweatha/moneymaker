from abc import ABC, abstractmethod

class CandleInterface(ABC):
    """
    Interface for a Candle object representing a financial candlestick.
    """

    @abstractmethod
    def isRed(self):
        """
        Check if the candlestick is red.

        Returns:
            bool: True if the candlestick is red, False otherwise.
        """
        pass

    @abstractmethod
    def isGreen(self):
        """
        Check if the candlestick is green.

        Returns:
            bool: True if the candlestick is green, False otherwise.
        """
        pass

    @abstractmethod
    def isDoji(self):
        """
        Check if the candlestick is a doji.

        Returns:
            bool: True if the candlestick is a doji, False otherwise.
        """
        pass

    @abstractmethod
    def isBt(self):
        """
        Check if the candlestick is a bottoming tail.

        Returns:
            bool: True if the candlestick meets the conditions for a trend reversal, False otherwise.
        """
        pass

    @abstractmethod
    def isTt(self):
        """
        Check if the candlestick is a topping tail.

        Returns:
            bool: True if the candlestick meets the conditions for a trend reversal, False otherwise.
        """
        pass