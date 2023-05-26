from abc import ABC, abstractmethod

class TrendInterface(ABC):
    """
    Interface for a Trend object.
    """

    @abstractmethod
    def findAllEma():
        """
        Calculate EMA (Exponential Moving Average) for the dict provided.
        """
        pass

    @abstractmethod
    def findAllTrend():
        """
        Analyze the trend from the EMA calculation data.
        """
        pass

    @abstractmethod
    def isSideways():
        """
        Check if trend is sideways.

        Returns:
            bool: True if trend is sideways, False otherwise.
        """
        pass

    @abstractmethod
    def isUptrend():
        """
        Check if trend is uptrend.

        Returns:
            bool: True if trend is uptrend, False otherwise.
        """
        pass