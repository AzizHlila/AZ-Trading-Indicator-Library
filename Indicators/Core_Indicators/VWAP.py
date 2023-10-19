import pandas as pd
import numpy as np


class VWAP:
    def VWAP(data:pd.DataFrame,Mode:str,MVWAP_WINDOW=1):
        
        '''
        ## Volume-Weighted Average Price (VWAP)
            mode values: 
                "typical" : (low+high+close)/3
                "close"   : close
        '''
        assert (Mode in ("typical","close")) ,"mode must be in ('typical','close')"

        df = data.copy(deep=True)

        # step one  (typical_price)
        if Mode == "typical":
            df["typical"]= (df["high"] +df["low"]+df["close"])/3

        # step two  ( volume X typical price )
        df["VxT"]   = df[Mode] * df["volume"]

        # step three ( Total (volume X typical price) ) and step four (Total V)
        totalVxT = df["VxT"].to_numpy()  # step 3
        totalV  = df["volume"].to_numpy() #step 4

        Date = df["date"].to_numpy()

        for i in range(1,totalVxT.size):
            if (Date[i]%86400000)!=0:   # skip new days
                totalVxT[i] += totalVxT[i-1] # step3
                totalV[i] += totalV[i-1] # step 4


        df["totalVxT"]=totalVxT
        df["totalV"]=totalV
        # finally step 5 ( calcule vwap (totalVxT /  totalV ) )

        df["vwap"] = df["totalVxT"] / df["totalV"]
        df["mvwap"] = df["vwap"].ewm(span=MVWAP_WINDOW,adjust=False).mean()
        return df[["vwap","mvwap"]]
    
