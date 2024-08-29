# Experimental version of the main.py code

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import plotly.graph_objs as go
import plotly.express as px
from tqdm import tqdm
from typing import List, Tuple
import talib

DATA_DIR = 'DATASETFOLDER_HERE'
BB_LENGTH = 20
BB_MULT = 2.0
KC_LENGTH = 20
KC_MULT = 1.5

def load_stock_data(directory: str) -> pd.DataFrame:
    all_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    data_list = []
    for file in tqdm(all_files, desc="Loading stock data", bar_format='{l_bar}{bar:30}{r_bar}{bar:-30b}'):
        df = pd.read_csv(file)
        df['date'] = pd.to_datetime(df['date'])
        data_list.append(df)
    return pd.concat(data_list, ignore_index=True)

def merge_sort(arr: List[float]) -> List[float]:
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left: List[float], right: List[float]) -> List[float]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def get_valid_ticker(data: pd.DataFrame) -> str:
    while True:
        ticker = input("Enter the stock ticker you want to analyze: ").upper()
        if ticker in data['ticker'].unique():
            return ticker
        else:
            print(f"No data available for ticker: {ticker}. Please try again.")

def calculate_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    data['sma_20'] = talib.SMA(data['close'], timeperiod=20)
    data['ema_50'] = talib.EMA(data['close'], timeperiod=50)
    data['rsi'] = talib.RSI(data['close'], timeperiod=14)
    data['macd'], data['macd_signal'], _ = talib.MACD(data['close'])
    
    data['upper_bb'], data['middle_bb'], data['lower_bb'] = talib.BBANDS(
        data['close'], 
        timeperiod=BB_LENGTH, 
        nbdevup=BB_MULT, 
        nbdevdn=BB_MULT
    )
    
    data['atr'] = talib.ATR(data['high'], data['low'], data['close'], timeperiod=KC_LENGTH)
    data['upper_kc'] = data['middle_bb'] + KC_MULT * data['atr']
    data['lower_kc'] = data['middle_bb'] - KC_MULT * data['atr']
    
    data['sqz_on'] = (data['lower_bb'] > data['lower_kc']) & (data['upper_bb'] < data['upper_kc'])
    data['sqz_off'] = (data['lower_bb'] < data['lower_kc']) & (data['upper_bb'] > data['upper_kc'])
    data['no_sqz'] = (~data['sqz_on']) & (~data['sqz_off'])
    
    data['linreg'] = talib.LINEARREG(data['close'], timeperiod=KC_LENGTH)
    data['sqz_mom'] = data['linreg'] - data['sma_20']
    
    return data

def train_model(X: pd.DataFrame, y: pd.Series) -> Tuple[RandomForestRegressor, float, float]:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    return model, mse, r2

def plot_predictions(data: pd.DataFrame, y_pred: np.ndarray, ticker: str):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data['date'], y=data['close'], mode='lines', name='Actual Close Price'))
    fig.add_trace(go.Scatter(x=data['date'], y=y_pred, mode='lines', name='Predicted Close Price', line=dict(color='red')))

    fig.update_layout(
        title=f'{ticker} Close Price Prediction',
        xaxis_title='Date',
        yaxis_title='Close Price',
        xaxis=dict(tickformat='%Y-%m-%d', tickangle=45)
    )

    fig.show()

def main():
    stock_data = load_stock_data(DATA_DIR)
    ticker = get_valid_ticker(stock_data)
    
    stock_data_filtered = stock_data[stock_data['ticker'] == ticker].sort_values(by='date')
    stock_data_filtered = calculate_technical_indicators(stock_data_filtered)
    
    features = ['sma_20', 'ema_50', 'rsi', 'macd', 'macd_signal', 'upper_bb', 'lower_bb', 
                'upper_kc', 'lower_kc', 'sqz_on', 'sqz_off', 'no_sqz', 'sqz_mom']
    X = stock_data_filtered[features].fillna(0)
    y = stock_data_filtered['close']
    
    model, mse, r2 = train_model(X, y)
    
    print(f"Model Performance:")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R-squared Score: {r2:.2f}")
    
    y_pred = model.predict(X)
    plot_predictions(stock_data_filtered, y_pred, ticker)

if __name__ == "__main__":
    main()
