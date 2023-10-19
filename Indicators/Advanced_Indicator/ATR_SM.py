from ..Core_Indicators.ATR import ATR
from ..Core_Indicators.MovingAverage import MA
import numpy as np
from pandas import Series

class ATR_SM:
    def ATR_SM_0(DF,Multiplier=6.3,Period=21,Smooth=100)->Series:
        """
        ## Average True Range (ATR) 
        """
        Tatr = ATR.ATR(DF,Period)
        Multiplier = 6.3
        nLoss = Tatr * Multiplier
        close = DF["close"].to_numpy()
        T2 = Tatr*0
        T2[0]=0
        for i in range(1,len(close)):
            if (close[i]>T2[i-1]) and (close[i-1]>T2[i-1]):
                T2[i] = max(T2[i-1],(close[i]-nLoss[i]))
            elif (close[i]<T2[i-1]) and (close[i-1]<T2[i-1]):
                T2[i] = min(T2[i-1],(close[i]+nLoss[i]))
            elif (close[i]>T2[i-1]): 
                T2[i] = (close[i]-nLoss[i])
            else:
                T2[i] = (close[i]+nLoss[i])
        DF["xATRTrailingStop"]=T2

        DF["out"]= MA.VWMA(DF["close"],DF["volume"],Smooth)

        DF["ATR_SM"]=np.average(DF[["out","xATRTrailingStop"]],axis=1)
        return DF["ATR_SM"]
