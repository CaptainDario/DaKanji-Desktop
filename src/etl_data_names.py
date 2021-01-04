from enum import Enum

class ETLDataNames(Enum):
    """An Enumeration which provides easy access to the ETL data set parts names.
    """

    ETL1  = "ETL1"
    """"""
    ETL2  = "ETL2"
    """"""
    ETL3  = "ETL3"
    """"""
    ETL4  = "ETL4"
    """"""
    ETL5  = "ETL5"
    """"""
    ETL6  = "ETL6"
    """"""
    ETL7  = "ETL7"
    """"""
    #provide the original naming...
    ETL8B = "ETL8"
    """Original name for ETL-8"""
    ETL8G = "ETL9"
    """Original name for ETL-9"""
    ETL9B = "ETL10"
    """Original name for ETL-10"""
    ETL9G = "ETL11"
    """Original name for ETL-11"""
    #...and the renamed alternative
    ETL8  = "ETL8"
    """Renamed ETL8B"""
    ETL9  = "ETL9"
    """Renamed ETL8G"""
    ETL10 = "ETL10"
    """Renamed ETL9B"""
    ETL11 = "ETL11"
    """Renamed ETL9G"""