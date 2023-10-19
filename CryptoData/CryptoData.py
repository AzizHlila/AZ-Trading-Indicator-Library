from time import time
from binance.client import Client
import pandas as pd
from threading import Thread



class Crypto_Data:

    def Download_One_Coin(Coin:str,TimeInerval:str='1m',client=None,ReturnList:list=None,ReturnIndex:int=None)-> pd.DataFrame:
        """
        Download Last 1000 info bars
        -1 : an error 

        * DF columns : date,open,high,low,close,volume
        """
    
        try:
            client = Client(testnet=False) if not client else client

            bars = client.get_klines(symbol=Coin, interval=TimeInerval,limit=1000)

            for line in bars:  # Keep only date and close columns, "date" "close"
                del line[6:]

            df = pd.DataFrame(bars, columns=['date','open','high','low','close','volume'])  # 2 dimensional tabular data

            # converstation to floats
            df["open"]=df["open"].astype(float)
            df["high"]=df["high"].astype(float)
            df["low"]=df["low"].astype(float)
            df["close"]=df["close"].astype(float)
            df["volume"]=df["volume"].astype(float)
            
            ## return methode
            # with return 
            if ReturnList==None:
                return df
            else:
                ReturnList[ReturnIndex] = df
        except:
            ReturnList[ReturnIndex]  = -1
            return -1

    def Download_Multi_Coins(CoinList:list,TimeInerval:str='1m')->dict:
        """
        type CoinList : List[str]
        type TimeInterval :str
        rtype : dict[pd.DataFrame]
        """
        try:
            client = Client(testnet=False)
        except :return -1


        T_threads = []
        ReturnList = list([0]*len(CoinList))
        for i,coin in enumerate(CoinList):
            th = Thread(target=Crypto_Data.Download_One_Coin,args=[coin,TimeInerval,client,ReturnList,i])
            T_threads.append(th)
            
        for th in T_threads:
            th.start()

        for th in T_threads:
            th.join()
        
        ResultDict ={}

        for i ,key in enumerate(CoinList):
            ResultDict[key] = ReturnList[i]

        return ResultDict
        


    def Download_Data_With_Size(Crypto_Symbol:str,TimeInerval:str='1m',DataLenght:int=2000)->pd.DataFrame:

        """
        * DF columns : date,open,high,low,close,volume
        """

        OneLength = Time_Calcule.ConvertStrTimeToSecond(TimeInerval)*1000

        StartDate =int(time()*1000)-( DataLenght * OneLength)

        client = Client()
        DATA =[]
        i = StartDate

        while DataLenght>0:
            if DataLenght>=1000:
                I_endTime = i+(OneLength*1000)
                DataLenght-=1000
            else:
                I_endTime = i+(OneLength*DataLenght)
                DataLenght=0


            bars = client.get_klines(symbol=Crypto_Symbol, interval=TimeInerval, startTime=i,endTime=I_endTime,limit=1000)
            i= I_endTime
            for line in bars:
                del line[6:]
            DATA+= bars

        df = pd.DataFrame(DATA, columns=['date','open','high','low','close','volume'])  # 2 dimensional tabular data

        # converstation to floats
        df["open"]=df["open"].astype(float)
        df["high"]=df["high"].astype(float)
        df["low"]=df["low"].astype(float)
        df["close"]=df["close"].astype(float)
        df["volume"]=df["volume"].astype(float)
        

        return df
    

    
class Time_Calcule:
    def ConvertStrTimeToSecond(ch:str)->int:
        '''
        m : minute
        h : hour
        #### exemples:
        * "5m" -> 60*5 s
        * "2h" -> 3600 * 2 s
        '''
        t=0
        while(ch and ch[0].isnumeric()):
            t*=10
            t+=int(ch[0])
            ch=ch[1:]
        
        if ch:
            if ch=="m":
                t*=60
            elif ch=="h":
                t*=3600
        return t