import numpy as np
from pandas import DataFrame



class MACD:
    def MACD(df:DataFrame,FAST_EMA=12,SLOW_EMA=26,SIGNAL=9)-> DataFrame:
        """
        return DataFrame["MACD","Signal","Histogram"]
        """


        # calculate Fast and Slow EMA mostly using close values
        FastEma = df['close'].ewm(span=FAST_EMA, adjust=False).mean()
        SlowEma = df['close'].ewm(span=SLOW_EMA, adjust=False).mean()

        # Calculate MACD and signal line
        MACD = FastEma - SlowEma
        signal = MACD.ewm(span=SIGNAL, adjust=False).mean()

        # put the MACD and signal lines in the Data
        df['MACD'] = MACD

        df['Signal'] = signal

        df['Trigger'] = np.where(df['MACD'] > df['Signal'], 1, 0)
        df['Position'] = df['Trigger'].diff()

        Histogram = (df['MACD'].to_numpy()) - (df['Signal'].to_numpy())

        df["Histogram"] = Histogram/Histogram.max()*100   # histogram values in -100 .. 100


        return df[["MACD","Signal","Histogram"]]

