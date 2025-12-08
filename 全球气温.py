
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False

url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts%2BdSST.csv"
df = pd.read_csv(url, skiprows=1)

df = df[['Year', 'J-D']]
df['J-D'] = pd.to_numeric(df['J-D'], errors='coerce')
df = df.dropna()

df['Year'] = df['Year'].astype(int)
df['Anomaly'] = df['J-D']
df = df[['Year', 'Anomaly']]
df['MA10'] = df['Anomaly'].rolling(window=10, center=True).mean()

plt.figure(figsize=(11, 6))
plt.plot(df['Year'], df['Anomaly'], color='red', label='年均温度异常 (°C)')
plt.plot(df['Year'], df['MA10'], color='black', linestyle='--', linewidth=2,
         label='10 年移动平均')

plt.xlabel("年份", fontsize=12)
plt.ylabel("温度异常 (°C)", fontsize=12)
plt.title("全球平均地表温度异常（NASA GISTEMP, 1880–至今）", fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig("global_temperature_trend_CN.png", dpi=300)
plt.show()
