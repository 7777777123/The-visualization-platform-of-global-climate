import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ===============================
# 1. 加载全球CO2数据（OWID）
# ===============================
co2_url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
co2_df = pd.read_csv(co2_url, low_memory=False)

co2_world = co2_df[co2_df['country'] == 'World'][["year", "co2"]]
co2_world = co2_world.rename(columns={"year": "Year", "co2": "Global_CO2"})
co2_world = co2_world[co2_world["Year"] >= 1960]

# ===============================
# 2. 加载全球温度异常数据（NASA GISTEMP）
# ===============================
temp_url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
temp_raw = pd.read_csv(temp_url, skiprows=1)

temp_df = temp_raw[["Year", "J-D"]].rename(columns={"J-D": "Temp_Anomaly"})
temp_df = temp_df.dropna()
temp_df = temp_df[temp_df["Year"] >= 1960]

# ===============================
# 3. 合并数据
# ===============================
df = pd.merge(co2_world, temp_df, on="Year", how="inner")

# ====== 🔥关键修复：确保数值为 float ======
df["Global_CO2"] = pd.to_numeric(df["Global_CO2"], errors="coerce")
df["Temp_Anomaly"] = pd.to_numeric(df["Temp_Anomaly"], errors="coerce")
df = df.dropna(subset=["Global_CO2", "Temp_Anomaly"])

# ===============================
# 4. 绘制散点图
# ===============================
plt.figure(figsize=(10, 6))

scatter = plt.scatter(
    df["Global_CO2"],
    df["Temp_Anomaly"],
    c=df["Year"],
    cmap="viridis",
    s=80,
    alpha=0.8
)

cbar = plt.colorbar(scatter)
cbar.set_label("年份 (Year)", fontsize=12)

# ===============================
# 5. 趋势线
# ===============================
z = np.polyfit(df["Global_CO2"], df["Temp_Anomaly"], 1)
p = np.poly1d(z)
plt.plot(df["Global_CO2"], p(df["Global_CO2"]), "r--", label="趋势线")

# ===============================
# 6. 美化图表
# ===============================
plt.title("全球变暖：CO₂ 排放量与全球气温异常（真实数据）", fontsize=16)
plt.xlabel("全球 CO₂ 排放量（百万吨/年）", fontsize=12)
plt.ylabel("全球温度异常（°C）", fontsize=12)
plt.grid(alpha=0.3)
plt.legend(fontsize=12)

plt.tight_layout()
plt.savefig("real_global_warming_scatter_fixed.png", dpi=300)
plt.show()
