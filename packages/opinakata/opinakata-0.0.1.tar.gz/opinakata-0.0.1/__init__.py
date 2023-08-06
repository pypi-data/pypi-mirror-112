def ACCBANDS(df):
    #df['AB_Middle_Band'] = pd.rolling_mean(df['Close'], 20)
    df['AB_Middle_Band'] = df['Close'].rolling(window = 20, center=False).mean()
    # High * ( 1 + 4 * (High - Low) / (High + Low))
    df['aupband'] = df['High'] * (1 + 4 * (df['High']-df['Low'])/(df['High']+df['Low']))
    df['AB_Upper_Band'] = df['aupband'].rolling(window=20, center=False).mean()
    # Low *(1 - 4 * (High - Low)/ (High + Low))
    df['adownband'] = df['Low'] * (1 - 4 * (df['High']-df['Low'])/(df['High']+df['Low']))
    df['AB_Lower_Band'] = df['adownband'].rolling(window=20, center=False).mean()
    return df

def acc_dist(data, trend_periods=21, open_col='Open', high_col='High', low_col='Low', close_col='Close', vol_col='Volume'):
    for index, row in data.iterrows():
        if row[high_col] != row[low_col]:
            ac = ((row[close_col] - row[low_col]) - (row[high_col] - row[close_col])) / (row[high_col] - row[low_col]) * row[vol_col]
        else:
            ac = 0
        data.at[index, 'acc_dist']= ac
    data['acc_dist_ema' + str(trend_periods)] = data['acc_dist'].ewm(ignore_na=False, min_periods=0, com=trend_periods, adjust=True).mean()
    
    return data

def kama(df, price, kama, n, fast_ema=2, slow_ema=30):

    er = (
        df[price].diff(n).abs()
        / df[price].diff().abs().rolling(window=n).sum()
    )
    fast_sc = 2 / (fast_ema + 1)
    slow_sc = 2 / (slow_ema + 1)
    df[kama + "_sc"] = ((er * (fast_sc - slow_sc)) + slow_sc) ** 2
    prev_kama = list(df[:n][price].rolling(window=n).mean())[-1]
    df.loc[n - 1, kama] = prev_kama
    df.loc[n:, kama] = 0.0
    kamas = [0.0 for i in range(n)]
    for row in df.loc[n:, [price, kama + "_sc"]].itertuples(index=False):
        kamas.append(prev_kama + row[1] * (row[0] - prev_kama))
        prev_kama = kamas[-1]
    df[kama] += kamas
    df = df.dropna().reset_index(drop=True)
    df.drop([kama + "_sc"], axis=1, inplace=True)

    return df

def ATR(data, trend_periods=14, open_col='Open', high_col='High', low_col='Low', close_col='Close', drop_tr = True):
    for index, row in data.iterrows():
        prices = [row[high_col], row[low_col], row[close_col], row[open_col]]
        if index > 0:
            val1 = np.amax(prices) - np.amin(prices)
            val2 = abs(np.amax(prices) - data.at[index - 1, close_col])
            val3 = abs(np.amin(prices) - data.at[index - 1, close_col])
            true_range = np.amax([val1, val2, val3])

        else:
            true_range = np.amax(prices) - np.amin(prices)

        data.at[index, 'true_range']= true_range
    data['ATR'] = data['true_range'].ewm(ignore_na=False, min_periods=0, com=trend_periods, adjust=True).mean()
    if drop_tr:
        data = data.drop(['true_range'], axis=1)
        
    return data

#ADX Function

def ADX(data, periods=14, high_col='High', low_col='Low'):
    remove_tr_col = False
    if not 'true_range' in data.columns:
        data = ATR(data, drop_tr = False)
        remove_tr_col = True

    data['m_plus'] = 0.
    data['m_minus'] = 0.
    
    for i,row in data.iterrows():
        if i>0:
            data.at[i, 'm_plus'] = (row[high_col] - data.at[i-1, high_col])
            data.at[i, 'm_minus'] = ( row[low_col] - data.at[i-1, low_col])
    
    data['dm_plus'] = 0.
    data['dm_minus'] = 0.
    
    for i,row in data.iterrows():
        if row['m_plus'] > row['m_minus'] and row['m_plus'] > 0:
            data.at[i, 'dm_plus']= row['m_plus']
            
        if row['m_minus'] > row['m_plus'] and row['m_minus'] > 0:
            data.at[i, 'dm_minus'] = row['m_minus']
    
    data['di_plus'] = (data['dm_plus'] / data['true_range']).ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean()
    data['di_minus'] = (data['dm_minus'] / data['true_range']).ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean()
    
    data['dxi'] = np.abs(data['di_plus'] - data['di_minus']) / (data['di_plus'] + data['di_minus'])
    data.at[0, 'dxi']=1.
    data['adx'] = data['dxi'].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean()
    data = data.drop(['m_plus', 'm_minus', 'dm_plus', 'dm_minus'], axis=1)
    if remove_tr_col:
        data = data.drop(['true_range'], axis=1)
         
    return data

def APTR(df,col_clo):
    df['APTR'] = (df['ATR']/col_clo) * 100
    return df
def AroonIndicator(df, col_high='High', col_low='Low', col_aroon='aroon', period_n=25):

    df[col_aroon + "_up"] = (
        df[col_high]
        .rolling(period_n)
        .apply(lambda x: float(np.argmax(x) + 1) / period_n * 100, raw=True)
    )
    df[col_aroon + "_dn"] = (
        df[col_low]
        .rolling(period_n)
        .apply(lambda x: float(np.argmin(x) + 1) / period_n * 100, raw=True)
    )
    df = df.dropna().reset_index(drop=True)

    return df
def AwesomeOscillator(signals):
    
    signals['awesome ma1'],signals['awesome ma2']=0,0
    signals['awesome ma1']=((signals['High']+signals['Low'])/2).rolling(window=5).mean()
    signals['awesome ma2']=((signals['High']+signals['Low'])/2).rolling(window=34).mean()
    
    return signals

def BalanceOfMarketPower(df, col_open='Open', col_high='High', col_low='Low', col_close='Close'):
    df['BOP'] = (df[col_close] - df[col_open]) / (df[col_high] - df[col_low])

    return df
def sma(df, window):
    sma = df.rolling(window = window).mean()
    return sma
# Compute the Bollinger Bands 
def bollinger_bands(df, sma, window):
    std = df.rolling(window = window).std()
    upper_bb = sma + std * 2
    lower_bb = sma - std * 2
    return upper_bb, lower_bb
def CamarillaPoints(data,col_low ='Low' , col_high='High' , col_clo='Close'):
    data['R4']  = data[col_clo] + ((data[col_high]-data[col_low]) * 1.5)
    data['R3']  = data[col_clo] + ((data[col_high]-data[col_low]) * 1.25)
    data['R2'] = data[col_clo] + ((data[col_high]-data[col_low]) * 1.166)
    data['R1']= data[col_clo] + ((data[col_high]-data[col_low]) * 1.083)
    data['PivotPoint'] = (data[col_high] +  data[col_low] + data[col_clo]) / 3
    data['S1']  = data[col_clo] -((data[col_high]-data[col_low]) * 1.083)
    data['S2']  = data[col_clo] - ((data[col_high]-data[col_low]) * 1.166)
    data['S3']  = data[col_clo] - ((data[col_high] -  data[col_low]) * 1.25)
    data['S4']  = data[col_clo] - ((data[col_high] -  data[col_low]) * 1.5)
    return data
def CCI(df, Period):
    TP = (df['High'] + df['Low'] + df['Close']) / 3
    df['CCI']= pd.Series((TP - TP.rolling(window=Period, center = False).mean()) / (0.015 * TP.rolling(window=Period, center=False).std()))
    return df
def chaikin_oscillator(data, periods_short=3, periods_long=10, high_col='High',
                       low_col='Low', close_col='Close', vol_col='Volume'):
    ac = pd.Series([])
    val_last = 0

    for index, row in data.iterrows():
        if row[high_col] != row[low_col]:
            val = val_last + ((row[close_col] - row[low_col]) - (row[high_col] - row[close_col])) / (row[high_col] - row[low_col]) * row[vol_col]
        else:
            val = val_last
        ac.at[index]=val
    val_last = val

    ema_long = ac.ewm(ignore_na=False, min_periods=0, com=periods_long, adjust=True).mean()
    ema_short = ac.ewm(ignore_na=False, min_periods=0, com=periods_short, adjust=True).mean()
    data['ch_osc'] = ema_short - ema_long

    return data
def chaikin_volatility(data, ema_periods=10, change_periods=10, high_col='High', low_col='Low', close_col='Close'):
    data['ch_vol_hl'] = data[high_col] - data[low_col]
    data['ch_vol_ema'] = data['ch_vol_hl'].ewm(ignore_na=False, min_periods=0, com=ema_periods, adjust=True).mean()
    data['chaikin_volatility'] = 0.
    
    for index,row in data.iterrows():
        if index >= change_periods:
            
            prev_value = data.at[index-change_periods, 'ch_vol_ema']
            if prev_value == 0:
                #this is to avoid division by zero below
                prev_value = 0.0001
            data.at [index, 'chaikin_volatility']= ((row['ch_vol_ema'] - prev_value)/prev_value)
            
    data = data.drop(['ch_vol_hl', 'ch_vol_ema'], axis=1)
        
    return data
def CloseLocationValue(df,col_hig,col_low,col_clo):
    df['CLV']=((df[col_clo]-df[col_low])-(df[col_hig]-df[col_clo]))/(df[col_hig]-df[col_low])
    return df
def DEMA(data,period,column):
    #Calculate the Exponential Moving Average (Ema)
    EMA = data[column].ewm(span=period,adjust=False).mean()
    #Calculate the DEMA 
    DEMA = 2*EMA-EMA.ewm(span=period,adjust=False).mean()
    data['DEMA']=DEMA
    return DEMA
def ease_of_movement(data, period=14, high_col='High', low_col='Low', vol_col='Volume'):
    for index, row in data.iterrows():
        if index > 0:
            midpoint_move = (row[high_col] + row[low_col]) / 2 - (data.at[index - 1, high_col] + data.at[index - 1, low_col]) / 2
        else:
            midpoint_move = 0
        
        diff = row[high_col] - row[low_col]

        if diff == 0:
            diff = 0.000000001
            
        vol = row[vol_col]
        if vol == 0:
            vol = 1
        box_ratio = (vol / 100000000) / (diff)
        emv = midpoint_move / box_ratio
        data.at[index, 'emv'] = emv
        
    data['emv_ema_'+str(period)] = data['emv'].ewm(ignore_na=False, min_periods=0, com=period, adjust=True).mean()
        
    return data
def EMA(data , period=20 , column='Close'):
    return data[column].ewm(span=period, adjust=False).mean()
def ForceIndex(data,col_clo='Close',col_vol='Volume',period_n=13): 
    FI = pd.Series(data['Close'].diff(period_n) * data['Volume'], name = 'ForceIndex') 
    data = data.join(FI) 
    return data
def ichimoku(df):
    # Turning Line
    period9_high = df['High'].rolling(window=9,center=False).max()
    period9_low = df['Low'].rolling(window=9,center=False).min()
    df['turning_line'] = (period9_high + period9_low) / 2
    
    # Standard Line
    period26_high = df['High'].rolling(window=26,center=False).max()
    period26_low = df['Low'].rolling(window=26,center=False).min()
    df['standard_line'] = (period26_high + period26_low) / 2
    
    # Leading Span 1
    df['ichimoku_span1'] = ((df['turning_line'] + df['standard_line']) / 2).shift(26)
    
    # Leading Span 2
    period52_high = df['High'].rolling(window=52,center=False).max()
    period52_low = df['Low'].rolling(window=52,center=False).min()
    df['ichimoku_span2'] = ((period52_high + period52_low) / 2).shift(26)
    
    # The most current closing price plotted 22 time periods behind (optional)
    df['chikou_span'] = df['Close'].shift(-22) # 22 according to investopedia
    return df
def KELCH(df, n):  
    df['KelChM'] = pd.Series(((df['High'] + df['Low'] + df['Close']) / 3).rolling(window =n, center=False).mean(), name = 'KelChM_' + str(n))  
    df['KelChU'] = pd.Series(((4 * df['High'] - 2 * df['Low'] + df['Close']) / 3).rolling(window =n, center=False).mean(), name = 'KelChU_' + str(n))  
    df['KelChD'] = pd.Series(((-2 * df['High'] + 4 * df['Low'] + df['Close']) / 3).rolling(window =n, center=False).mean(), name = 'KelChD_' + str(n))    
    return df
def MACD(data,period_long=26, period_short =12 , period_signal=9 , column='Close'):
    # Calculate the short term Exponential Moving Average
    ShortEMA = EMA(data, period_short, column=column)
    # Calculate the Long term Exponential Moving Average
    LongEMA  = EMA(data, period_long, column=column)
    # Calculate the Moving Average Convergence/Divergence : 
    data['MACD'] = ShortEMA - LongEMA
    # Calculate The Signal Line : 
    data['Signal_Line'] = EMA(data , period_signal , column='MACD')
    return data 
def mass_index(data, period=25, ema_period=9, high_col='High', low_col='Low'):
    high_low = data[high_col] - data[low_col] + 0.000001 # Pour Evité la division par 0
    ema = high_low.ewm(ignore_na=False, min_periods=0, com=ema_period, adjust=True).mean()
    ema_ema = ema.ewm(ignore_na=False, min_periods=0, com=ema_period, adjust=True).mean()
    div = ema / ema_ema

    for index, row in data.iterrows():
        if index >= period:
            val = div[index-25:index].sum()
        else:
            val = 0
        data.at[index, 'mass_index'] = val
         
    return data
def MINMAX(df,volume='Volume'):
    df['MIN_Volume'] = df['Volume'].rolling(window=14,center=False).min()
    df['MAX_Volume'] = df['Volume'].rolling(window=14,center=False).max()
    return df
def momentum(data, periods=14, close_col='Close'):
    """periods: period for calculating momentum
    close_col: the name of the CLOSE values column"""
    data['momentum'] = 0.
    
    for index,row in data.iterrows():
        if index >= periods:
            prev_close = data.at[index-periods, close_col]
            val_perc = (row[close_col] - prev_close)/prev_close

            data.at[index, 'momentum'] = val_perc

    return data
def typical_price(data, high_col = 'High', low_col = 'Low', close_col = 'Close'):
    
    data['typical_price'] = (data[high_col] + data[low_col] + data[close_col]) / 3

    return data


def money_flow_index(data, periods=14, vol_col='Volume'):
    remove_tp_col = False
    if not 'typical_price' in data.columns:
        data = typical_price(data)
        remove_tp_col = True
    
    data['money_flow'] = data['typical_price'] * data[vol_col]
    data['money_ratio'] = 0.
    data['money_flow_index'] = 0.
    data['money_flow_positive'] = 0.
    data['money_flow_negative'] = 0.
    
    for index,row in data.iterrows():
        if index > 0:
            if row['typical_price'] < data.at[index-1, 'typical_price']:
                data.at[index, 'money_flow_positive'] = row['money_flow']
            else:
                data.at[index, 'money_flow_negative'] =  row['money_flow']
    
        if index >= periods:
            period_slice = data['money_flow'][index-periods:index]
            positive_sum = data['money_flow_positive'][index-periods:index].sum()
            negative_sum = data['money_flow_negative'][index-periods:index].sum()

            if negative_sum == 0.:

                negative_sum = 0.00001
            m_r = positive_sum / negative_sum

            mfi = 1-(1 / (1 + m_r))

            data.at[index, 'money_ratio']= m_r
            data.at[index, 'money_flow_index']= mfi
          
    data = data.drop(['money_flow', 'money_ratio', 'money_flow_positive', 'money_flow_negative'], axis=1)
    
    if remove_tp_col:
        data = data.drop(['typical_price'], axis=1)

    return data
def psar(df, iaf = 0.02, maxaf = 0.2,date='Local time'):
    length = len(df)
    dates = date
    high = (df['High'])
    low = (df['Low'])
    close = (df['Close'])
    psar = df['Close'][0:len(df['Close'])]
    psarbull = [None] * length
    psarbear = [None] * length
    bull = True
    af = iaf
    ep = df['Low'][0]
    hp = df['High'][0]
    lp = df['Low'][0]
    for i in range(2,length):
        if bull:
            psar[i] = psar[i - 1] + af * (hp - psar[i - 1])
        else:
            psar[i] = psar[i - 1] + af * (lp - psar[i - 1])
        reverse = False
        if bull:
            if df['Low'][i] < psar[i]:
                bull = False
                reverse = True
                psar[i] = hp
                lp = df['Low'][i]
                af = iaf
        else:
            if df['High'][i] > psar[i]:
                bull = True
                reverse = True
                psar[i] = lp
                hp = df['High'][i]
                af = iaf
        if not reverse:
            if bull:
                if df['High'][i] > hp:
                    hp = df['High'][i]
                    af = min(af + iaf, maxaf)
                if df['Low'][i - 1] < psar[i]:
                    psar[i] = df['Low'][i - 1]
                if df['Low'][i - 2] < psar[i]:
                    psar[i] = df['Low'][i - 2]
            else:
                if df['Low'][i] < lp:
                    lp = df['Low'][i]
                    af = min(af + iaf, maxaf)
                if df['High'][i - 1] > psar[i]:
                    psar[i] = df['High'][i - 1]
                if df['High'][i - 2] > psar[i]:
                    psar[i] = df['High'][i - 2]
        if bull:
            psarbull[i] = psar[i]
        else:
            psarbear[i] = psar[i]
    #return {"dates":dates, "high":high, "low":low, "close":close, "psar":psar, "psarbear":psarbear, "psarbull":psarbull}
    #return psar, psarbear, psarbull
    df['psar'] = psar
    return df
    #df['psarbear'] = psarbear
    #df['psarbull'] = psarbull
def positive_volume_index(data, periods=255, close_col='Close', vol_col='Volume'):
    data['pvi'] = 0.
    
    for index,row in data.iterrows():
        if index > 0:
            prev_pvi = data.at[index-1, 'pvi']
            prev_close = data.at[index-1, close_col]
            if row[vol_col] > data.at[index-1, vol_col]:
                pvi = prev_pvi + (row[close_col] - prev_close / prev_close * prev_pvi)
            else: 
                pvi = prev_pvi
        else:
            pvi = 1000
        data.at[index, 'pvi']=pvi
    data['pvi_ema'] = data['pvi'].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean()

    return data
def ROC(data,col_clo='Close',period_n=14):
    N = data[col_clo].diff(period_n)
    D = data[col_clo].shift(period_n)
    ROC = pd.Series(N/D,name='Rate of Change')
    data = data.join(ROC)
    return data 
def SMA(data , period=30 , column='Close'):
    return data[column].rolling(window=period).mean()
# Create a function to compute the relative strength index (RSI)
def RSI(data, period=14 , column='Close'):
    delta = data[column].diff(1) # diff utilisé pour trouver le discret difference sur l'axe des colonne avec une valeur de periode par defaut =1
    delta = delta[1:]
    up = delta.copy()
    down = delta.copy()
    up[up<0] = 0
    down[down>0] = 0
    data['up'] = up
    data['down'] = down
    AVG_Gain = SMA(data , period, column='up')
    AVG_Loss = abs(SMA(data , period, column='down'))
    RS = AVG_Gain/AVG_Loss
    RSI = 100.0 - (100.0 / (1.0 + RS))
    data['RSI'] = RSI 
    return data 
def trix(data, periods=14, signal_periods=9, close_col='Close'):
    data['trix'] = data[close_col].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean()
    data['trix'] = data['trix'].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean()
    data['trix'] = data['trix'].ewm(ignore_na=False, min_periods=0, com=periods, adjust=True).mean()
    data['trix_signal'] = data['trix'].ewm(ignore_na=False, min_periods=0, com=signal_periods, adjust=True).mean()
        
    return data
def williams_ad(data, high_col='High', low_col='Low', close_col='Close'):
    data['williams_ad'] = 0.
    
    for index,row in data.iterrows():
        if index > 0:
            prev_value = data.at[index-1, 'williams_ad']
            prev_close = data.at[index-1, close_col]
            if row[close_col] > prev_close:
                ad = row[close_col] - min(prev_close, row[low_col])
            elif row[close_col] < prev_close:
                ad = row[close_col] - max(prev_close, row[high_col])
            else:
                ad = 0.
                                                                                                        
            data.at[index, 'williams_ad']= (ad+prev_value)
        
    return data
def williams_r(data, periods=14, high_col='High', low_col='Low', close_col='Close'):
    data['williams_r'] = 0.
    
    for index,row in data.iterrows():
        if index > periods:
            data.at[index, 'williams_r']= ((max(data[high_col][index-periods:index]) - row[close_col]) / 
                                                 (max(data[high_col][index-periods:index]) - min(data[low_col][index-periods:index])))
        
    return data
