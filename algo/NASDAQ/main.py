import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import plotly.graph_objs as go
import plotly.express as px
from tqdm import tqdm

data_dir = 'DATASETFOLDER_HERE'


def load_stock_data(directory):
    all_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    data_list = []
    for file in tqdm(all_files, desc="Loading stock data", bar_format='{l_bar}{bar:30}{r_bar}{bar:-30b}'):
        data_list.append(pd.read_csv(file))
    return pd.concat(data_list, ignore_index=True)


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sorted_arrays(arr1, arr2):
    sorted_array = []
    i = j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            sorted_array.append(arr1[i])
            i += 1
        else:
            sorted_array.append(arr2[j])
            j += 1
    sorted_array.extend(arr1[i:])
    sorted_array.extend(arr2[j:])
    return sorted_array


def split_and_merge_sort(arr, split_size=10):
    sub_arrays = [arr[i:i + split_size] for i in range(0, len(arr), split_size)]

    for i in range(len(sub_arrays)):
        sub_arrays[i] = insertion_sort(sub_arrays[i])

    while len(sub_arrays) > 1:
        merged_arrays = []
        for i in range(0, len(sub_arrays), 2):
            if i + 1 < len(sub_arrays):
                merged_arrays.append(merge_sorted_arrays(sub_arrays[i], sub_arrays[i + 1]))
            else:
                merged_arrays.append(sub_arrays[i])
        sub_arrays = merged_arrays

    return sub_arrays[0] if sub_arrays else []


stock_data = load_stock_data(data_dir)


def get_valid_ticker(data):
    while True:
        ticker = input("Enter the stock ticker you want to analyze: ").upper()
        if ticker in data['ticker'].unique():
            return ticker
        else:
            print(f"No data available for ticker: {ticker}. Please try again.")


ticker = get_valid_ticker(stock_data)

stock_data_filtered = stock_data[stock_data['ticker'] == ticker].sort_values(by='date')


def calculate_squeeze_momentum(data, bb_length=20, bb_mult=2.0, kc_length=20, kc_mult=1.5):
    tqdm.pandas(desc="Calculating Bollinger Bands", bar_format='{l_bar}{bar:30}{r_bar}{bar:-30b}')
    data['sma_bb'] = data['close'].rolling(window=bb_length).mean()
    data['std_bb'] = data['close'].rolling(window=bb_length).std()
    data['upper_bb'] = data['sma_bb'] + bb_mult * data['std_bb']
    data['lower_bb'] = data['sma_bb'] - bb_mult * data['std_bb']

    data['sma_kc'] = data['close'].rolling(window=kc_length).mean()
    tr = np.maximum(data['high'] - data['low'], np.abs(data['high'] - data['close'].shift()),
                    np.abs(data['low'] - data['close'].shift()))
    data['atr'] = tr.rolling(window=kc_length).mean()
    data['upper_kc'] = data['sma_kc'] + kc_mult * data['atr']
    data['lower_kc'] = data['sma_kc'] - kc_mult * data['atr']

    data['sqz_on'] = (data['lower_bb'] > data['lower_kc']) & (data['upper_bb'] < data['upper_kc'])
    data['sqz_off'] = (data['lower_bb'] < data['lower_kc']) & (data['upper_bb'] > data['upper_kc'])
    data['no_sqz'] = (~data['sqz_on']) & (~data['sqz_off'])

    data['linreg'] = data['close'].rolling(window=kc_length).apply(lambda x: np.polyfit(range(kc_length), x, 1)[0],
                                                                   raw=True)
    data['sqz_mom'] = data['linreg'] - data['close'].rolling(window=kc_length).mean()

    return data


stock_data_filtered = calculate_squeeze_momentum(stock_data_filtered)

features = ['upper_bb', 'lower_bb', 'upper_kc', 'lower_kc', 'sqz_on', 'sqz_off', 'no_sqz', 'sqz_mom']
X = stock_data_filtered[features].fillna(0)
y = stock_data_filtered['close']

print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training the model...")
model = LinearRegression()
model.fit(X_train, y_train)

print("Making predictions...")
y_pred = model.predict(X_test)

subset_size = 100
subset_data = stock_data_filtered.iloc[-subset_size:]

X_subset = subset_data[features].fillna(0)
y_subset = subset_data['close']

model_subset = LinearRegression()
model_subset.fit(X_subset, y_subset)

y_subset_pred = model_subset.predict(X_subset)

fig = go.Figure()

fig.add_trace(go.Scatter(x=subset_data['date'], y=subset_data['close'], mode='lines', name='Actual Close Price'))
fig.add_trace(go.Scatter(x=subset_data['date'], y=y_subset_pred, mode='lines', name='Predicted Close Price',
                         line=dict(color='red')))

fig.update_layout(
    title=f'{ticker} Close Price Prediction (Last 100 Days)',
    xaxis_title='Date',
    yaxis_title='Close Price',
    xaxis=dict(tickformat='%Y-%m-%d', tickangle=45)
)

fig.show()
