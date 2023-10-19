import pandas as pd
import numpy as np


class RSI:
    def RSI(src:pd.Series,WINDOW_LENGTH=14,SMA_WINDOW=1)->pd.DataFrame:


        close =src.to_numpy()

        # time window

        diff = np.diff(close)
        up_chg = 0 * diff
        down_chg = 0 * diff

        # up change is equal to the positive difference, otherwise equal to zero
        up_chg[diff > 0] = diff[diff > 0]

        # down change is equal to negative deifference, otherwise equal to zero
        down_chg[diff < 0] = diff[diff < 0]

        up_chg = pd.DataFrame(up_chg)
        down_chg = pd.DataFrame(down_chg)

        up_chg_avg = up_chg.ewm(com=WINDOW_LENGTH - 1, min_periods=WINDOW_LENGTH).mean()
        down_chg_avg = down_chg.ewm(com=WINDOW_LENGTH - 1, min_periods=WINDOW_LENGTH).mean()

        rs = abs(up_chg_avg / down_chg_avg)
        rsi = 100 - 100 / (1 + rs)

        df=pd.DataFrame(rsi.to_numpy(),columns=["rsi"])
        if SMA_WINDOW>1:
            rsi_sma =  rsi.rolling(SMA_WINDOW).mean()
            df["rsi_sma"]=rsi_sma
            
        return df
