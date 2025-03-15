import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression  # scikit-learn
print('hello')

df = pd.read_csv('dane\\weight-height.csv', sep=';')
print(f'typ: {type(df)}')
print(df)