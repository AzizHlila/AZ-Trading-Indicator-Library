import pandas as pd
from .MovingAverage import MA

class ATR:
    def ATR(DF:pd.DataFrame, n=14) -> pd.Series:
        """
        * DF columns : date,open,high,low,close,volume
        """

        data = DF.copy()
        high = data["high"]
        low = data["low"]
        close = data["close"]
        data['tr0'] = abs(high - low)
        data['tr1'] = abs(high - close.shift())
        data['tr2'] = abs(low - close.shift())
        tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
        atr = MA.WMA(tr,n)
        return atr
