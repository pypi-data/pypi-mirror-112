# -*- coding: utf-8 -*-

from fbprophet import Prophet
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from fbprophet.plot import add_changepoints_to_plot

def Forcast_Time_Serise(df,freq='1d',periods=30):
    df.columns = ['ds','y']
    df['ds'] = pd.to_datetime(df['ds'],unit='s')
    df['y'] = (df['y'] - df['y'].mean()) / (df['y'].std())
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=periods, freq=freq)
    future.tail()
    forecast = m.predict(future)
    fig = m.plot(forecast)
    a = add_changepoints_to_plot(fig.gca(), m, forecast)
    m.plot_components(forecast)
    x1 = forecast['ds']
    y1 = forecast['yhat']
    y2 = forecast['yhat_lower']
    y3 = forecast['yhat_upper']
    plt.plot(x1,y1)
    plt.plot(x1,y2)
    plt.plot(x1,y3)
    plt.show()
    print('所有预测结果为：\n',forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
    print('最后五个预测结果为：\n',forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())