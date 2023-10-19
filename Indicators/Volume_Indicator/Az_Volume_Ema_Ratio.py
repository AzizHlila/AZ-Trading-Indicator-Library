from pandas import Series
import numpy as np

class AzVolumeEmaRatio:
    def BigVolume(DataVolume:Series,VolEma:int=4,Ratio:float=1.5)->Series:
        
        ema = lambda src,window: src.ewm(span=window,adjust=False).mean()
        VolEma= ema(DataVolume,4)
        VolRatio = np.where(DataVolume>VolEma*Ratio,1,0)

        return VolRatio

        