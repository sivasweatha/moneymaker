from abc import ABC, abstractmethod

class StrategyInterface(ABC):
    """
    Interface for a Strategy object.
    """

    @abstractmethod
    def CPR():
        """
        Calculate the CPR and support/resistance zones.

        Returns:
            dict: Containing all the CPR points.
        """
        pass

    @abstractmethod
    def isBull180():
        """
        Check if the pattern is a Bull180.

        Returns:
            bool: True if it is a Bull180, False otherwise.
        """
        pass

    @abstractmethod
    def isBear180():
        """
        Check if the pattern is a Bear180.

        Returns:
            bool: True if the pattern is a Bear180, False otherwise.
        """
        pass

    @abstractmethod
    def isGbi():
        """
        Check if the pattern is a Green Bar Ignored.

        Returns:
            bool: True if the pattern is GBI, False otherwise.
        """
        pass

    @abstractmethod
    def isRbi():
        """
        Check if the pattern is Red Bar Ignored

        Returns:
            bool: True if the pattern is RBI, False otherwise.
        """
        pass