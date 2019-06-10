import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import xlwings as xw

print('Loading data...')
wb = xw.Book('Holt_Winters_Data.xlsx').sheets['Tabelle1']
print('Loading completed')
train = np.asarray(wb.range('C2:C41').value)

model = ExponentialSmoothing(train, seasonal='mul',  seasonal_periods=12).fit()
pred = model.predict(start=0, end=47)

plt.plot(np.arange(0,len(train)), train, label='Train')
plt.plot(np.arange(0,len(pred)), pred, label='Holt-Winters')
plt.legend(loc='best')
plt.show()
