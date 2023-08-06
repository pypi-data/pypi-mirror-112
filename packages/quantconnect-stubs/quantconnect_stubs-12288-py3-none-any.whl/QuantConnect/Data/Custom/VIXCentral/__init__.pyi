import datetime
import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Custom.VIXCentral
import System.Collections.Generic


class VIXCentralContango(QuantConnect.Data.BaseData):
    """VIXCentral Contango"""

    @property
    def FrontMonth(self) -> int:
        """The month of the front month contract (possible values: 1 - 12)"""
        ...

    @FrontMonth.setter
    def FrontMonth(self, value: int):
        """The month of the front month contract (possible values: 1 - 12)"""
        ...

    @property
    def F1(self) -> float:
        """Front month contract"""
        ...

    @F1.setter
    def F1(self, value: float):
        """Front month contract"""
        ...

    @property
    def F2(self) -> float:
        """Contract 1 month away from the front month contract"""
        ...

    @F2.setter
    def F2(self, value: float):
        """Contract 1 month away from the front month contract"""
        ...

    @property
    def F3(self) -> float:
        """Contract 2 months away from the front month contract"""
        ...

    @F3.setter
    def F3(self, value: float):
        """Contract 2 months away from the front month contract"""
        ...

    @property
    def F4(self) -> float:
        """Contract 3 months away from the front month contract"""
        ...

    @F4.setter
    def F4(self, value: float):
        """Contract 3 months away from the front month contract"""
        ...

    @property
    def F5(self) -> float:
        """Contract 4 months away from the front month contract"""
        ...

    @F5.setter
    def F5(self, value: float):
        """Contract 4 months away from the front month contract"""
        ...

    @property
    def F6(self) -> float:
        """Contract 5 months away from the front month contract"""
        ...

    @F6.setter
    def F6(self, value: float):
        """Contract 5 months away from the front month contract"""
        ...

    @property
    def F7(self) -> float:
        """Contract 6 months away from the front month contract"""
        ...

    @F7.setter
    def F7(self, value: float):
        """Contract 6 months away from the front month contract"""
        ...

    @property
    def F8(self) -> float:
        """Contract 7 months away from the front month contract"""
        ...

    @F8.setter
    def F8(self, value: float):
        """Contract 7 months away from the front month contract"""
        ...

    @property
    def F9(self) -> typing.Optional[float]:
        """Contract 8 months away from the front month contract"""
        ...

    @F9.setter
    def F9(self, value: typing.Optional[float]):
        """Contract 8 months away from the front month contract"""
        ...

    @property
    def F10(self) -> typing.Optional[float]:
        """Contract 9 months away from the front month contract"""
        ...

    @F10.setter
    def F10(self, value: typing.Optional[float]):
        """Contract 9 months away from the front month contract"""
        ...

    @property
    def F11(self) -> typing.Optional[float]:
        """Contract 10 months away from the front month contract"""
        ...

    @F11.setter
    def F11(self, value: typing.Optional[float]):
        """Contract 10 months away from the front month contract"""
        ...

    @property
    def F12(self) -> typing.Optional[float]:
        """Contract 11 months away from the front month contract"""
        ...

    @F12.setter
    def F12(self, value: typing.Optional[float]):
        """Contract 11 months away from the front month contract"""
        ...

    @property
    def Contango_F2_Minus_F1(self) -> float:
        """Percentage change between contract F2 and F1, calculated as: (F2 - F1) / F1"""
        ...

    @Contango_F2_Minus_F1.setter
    def Contango_F2_Minus_F1(self, value: float):
        """Percentage change between contract F2 and F1, calculated as: (F2 - F1) / F1"""
        ...

    @property
    def Contango_F7_Minus_F4(self) -> float:
        """Percentage change between contract F7 and F4, calculated as: (F7 - F4) / F4"""
        ...

    @Contango_F7_Minus_F4.setter
    def Contango_F7_Minus_F4(self, value: float):
        """Percentage change between contract F7 and F4, calculated as: (F7 - F4) / F4"""
        ...

    @property
    def Contango_F7_Minus_F4_Div_3(self) -> float:
        """Percentage change between contract F7 and F4 divided by 3, calculated as: ((F7 - F4) / F4) / 3"""
        ...

    @Contango_F7_Minus_F4_Div_3.setter
    def Contango_F7_Minus_F4_Div_3(self, value: float):
        """Percentage change between contract F7 and F4 divided by 3, calculated as: ((F7 - F4) / F4) / 3"""
        ...

    @property
    def Period(self) -> datetime.timedelta:
        """The timespan that each data point covers"""
        ...

    @Period.setter
    def Period(self, value: datetime.timedelta):
        """The timespan that each data point covers"""
        ...

    @property
    def EndTime(self) -> datetime.datetime:
        """The ending time of the data point"""
        ...

    @EndTime.setter
    def EndTime(self, value: datetime.datetime):
        """The ending time of the data point"""
        ...

    def __init__(self) -> None:
        """Creates a new instance of the object"""
        ...

    def DefaultResolution(self) -> int:
        """
        Gets the default resolution for this data and security type
        
        :returns: This method returns the int value of a member of the QuantConnect.Resolution enum.
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """Gets the source location of the VIXCentral data"""
        ...

    def IsSparseData(self) -> bool:
        """
        Determines if data source is sparse
        
        :returns: false.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reads the data from the source and creates a BaseData instance
        
        :param config: Configuration
        :param line: Line of data
        :param date: Date we're requesting data for
        :param isLiveMode: Is live mode
        :returns: New BaseData instance to be used in the algorithm.
        """
        ...

    def RequiresMapping(self) -> bool:
        """
        Determines whether the data source requires mapping
        
        :returns: false.
        """
        ...

    def SupportedResolutions(self) -> System.Collections.Generic.List[QuantConnect.Resolution]:
        """Gets the supported resolution for this data and security type"""
        ...

    def ToString(self) -> str:
        """
        Converts the instance to a string
        
        :returns: String containing open, high, low, close.
        """
        ...


