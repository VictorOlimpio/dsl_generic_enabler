import pandas as pd
import os
import matplotlib.pyplot as plt

DOC_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))) + '/dsl_layer/datasets/'

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))

df1 = pd.read_csv(DOC_DIR + 'resultado.csv', sep=';')
df1.rename(columns={'mean_mse_[M0]': 'mse_knn', 'mean_mae_[M0]': 'mae_knn',
                    'mean_mse_[M1]': 'mse_ht', 'mean_mae_[M1]': 'mae_ht'}, inplace=True)
df1.plot(ax=axes[0,0], y=[
    'mse_knn', 'mae_knn'], grid=True, kind='line', title='KNN EvaluatePrequential Results', logy=True)

df1.plot(ax=axes[0,1], y=[
    'mse_ht', 'mae_ht'], grid=True, kind='line', title='HT EvaluatePrequential Results', logy=True)
df2 = pd.read_csv(DOC_DIR + 'resultado_knn.csv', sep=';')
df2.rename(columns={'current_mae': 'mae_knn', 'current_mse': 'mse_knn'}, inplace=True)
df2.plot(ax=axes[1,0], x='total_samples', y=[
         'mse_knn', 'mae_knn'], grid=True, kind='line', title='KNN DSLGE Results', logy=True)

df3 = pd.read_csv(DOC_DIR + 'resultado_ht.csv', sep=';')
df3.rename(columns={'current_mae': 'mae_ht', 'current_mse': 'mse_ht'}, inplace=True)
df3.plot(ax=axes[1,1], x='total_samples', y=[
         'mse_ht', 'mae_ht'], grid=True, kind='line', title='HT DSLGE Results', logy=True)
plt.show()
print(df1.tail())
print(df2.tail())
print(df3.tail())