import pandas as pd

class MA:
    def SMA(src:pd.Series,Window:int)->pd.Series:
        """
        ## Simple moving average
        """
        return src.rolling(Window).mean()
    
    def EMA(src:pd.Series,Window:int)->pd.Series:
        """
        ## Exponential moving average
        """
        return src.ewm(span=Window,adjust=False).mean()

    def VWMA(src:pd.Series,volume_src:pd.Series,period=100)->pd.Series:
        """
        ## Volume Weighted Moving Average (VWMA)
        """
        return (src*volume_src).rolling(window=period).mean()/(volume_src).rolling(window=period).mean()

    def WMA(src:pd.Series, n) -> pd.Series:
        """
        ## Weighted Moving Average (WMA)
        """
        return src.ewm(alpha=1/n, adjust=False).mean()
