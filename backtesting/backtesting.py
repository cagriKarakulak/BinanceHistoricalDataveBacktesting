from ta.trend import MACD
import pandas as pd
import winsound
duration = 1000  # milliseconds
freq = 440  # Hz
longIslemde = False
shortIslemde = False
anaPara = 100
islemSayisi = 0
win = 0
loss = 0
enDusukPara = anaPara
enYuksekPara = anaPara
winRate = 0
longEnterZaman = 0 
shortEnterZaman = 0
longEnterFiyat = 0
longExitFiyat = 0


csvName = "BTCUSDT2020-2021.csv"

print("BACKTEST HAZIRLANIYOR...")
attributes = ["timestamp","open","high","low","close","volume","1","2","3","4","5","6"]
df = pd.read_csv(csvName, names = attributes)

macdDiff= MACD(df["close"],26,12,9)
df["Macd Diff"] = macdDiff.macd_diff()


for i in range(df.shape[0]):
    print(str(len(df.index)) + "/" + str(i) , " Backtest yapılıyor... Ana Para: ", anaPara)
    if i > 26:
        # BULL EVENT
        if float(df["Macd Diff"][i-1]) > 0:
            # SHORT EXIT
            if shortIslemde == True:
                shortExitFiyat = float(df["open"][i])
                anaPara = anaPara + (((anaPara / 100) * ((longExitFiyat - longEnterFiyat) / longEnterFiyat) * 100)) * -1
                #anaPara = anaPara * 0.9996
                if anaPara < enDusukPara:
                    enDusukPara = anaPara
                if anaPara > enDusukPara:
                    enDusukPara = enDusukPara
                if enYuksekPara < anaPara:
                    enYuksekPara = anaPara
                if enYuksekPara > anaPara:
                    enYuksekPara = enYuksekPara
                islemSayisi = islemSayisi + 1
                if shortExitFiyat < shortEnterFiyat:
                    win = win + 1
                else: loss = loss + 1
                winRate = (win / islemSayisi) * 100
                shortIslemde = False  
            
            # LONG ENTER   
            if longIslemde == False and anaPara > 5:
                longEnterFiyat = float(df["open"][i])
                #anaPara = anaPara * 0.9996
                longIslemde = True
        
            if anaPara < 5:
                print("Bakiye Yetersiz...")
    
        #BEAR EVENT
        if float(df["Macd Diff"][i-1]) < 0:
        
            # LONG EXIT
            if longIslemde == True:
                longExitFiyat = float(df["open"][i])
                anaPara = anaPara + ((anaPara / 100) * ((longExitFiyat - longEnterFiyat) / longEnterFiyat) * 100)
                #anaPara = anaPara * 0.9996
                if anaPara < enDusukPara:
                    enDusukPara = anaPara
                if anaPara > enDusukPara:
                    enDusukPara = enDusukPara
                if enYuksekPara < anaPara:
                    enYuksekPara = anaPara
                if enYuksekPara > anaPara:
                    enYuksekPara = enYuksekPara
                islemSayisi = islemSayisi + 1
                if longExitFiyat > longEnterFiyat:
                    win = win + 1
                else: loss = loss + 1
                winRate = (win / islemSayisi) * 100
                longIslemde = False
        
            # SHORT ENTER
            if shortIslemde == False and anaPara > 5:
                shortEnterFiyat = float(df["open"][i])
                shortIslemde = True
                #anaPara = anaPara * 0.9996
            if anaPara < 5:
                print("Bakiye Yetersiz...")
        
print("BACKTEST BİTTİ. SONUÇLAR: ")
print(csvName)
print("Toplam Para: ", anaPara)
print("En Düşük Para: ", enDusukPara)
print("En Yüksek Para: ", enYuksekPara)
print("Tamamlanan İşlem Sayısı: ", islemSayisi)
print("Win: ", win, " Loss: ", loss, " Win Rate: " , winRate)
winsound.Beep(freq, duration)