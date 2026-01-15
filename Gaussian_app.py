import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 页面配置 ---
st.set_page_config(page_title="高斯光束仿真实验室", layout="centered")

st.title("🔦 交互式光学实验室：高斯光束")
st.markdown("调整左侧参数，观察高斯光束的束腰变化。")

# --- 1. 侧边栏：参数输入 ---
with st.sidebar:
    st.header("参数设置")
    w0 = st.slider("束腰半径 w0 (μm)", 1.0, 50.0, 10.0)
    lam = st.slider("波长 λ (μm)", 0.4, 1.55, 0.632) # 默认 632.8nm
    z_max = st.slider("传播距离 Z (mm)", 1.0, 100.0, 10.0)

# --- 2. 物理计算 (NumPy) ---
z = np.linspace(-z_max, z_max, 500) * 1000  # 换算成 um
z_r = (np.pi * w0**2) / lam # 瑞利长度
w_z = w0 * np.sqrt(1 + (z / z_r)**2) # 束宽随 z 的变化

# --- 3. 绘图 (Matplotlib) ---
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(z/1000, w_z, 'b', label='Beam Radius w(z)')
ax.plot(z/1000, -w_z, 'b')
ax.fill_between(z/1000, w_z, -w_z, color='blue', alpha=0.1)

# 装饰图表
ax.set_title(f"Gaussian Beam Propagation (λ={lam}μm, w0={w0}μm)")
ax.set_xlabel("Propagation Distance z (mm)")
ax.set_ylabel("Beam Radius w (μm)")
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()

# --- 4. 在网页展示 ---
st.pyplot(fig)

# 显示一些计算结果
col1, col2 = st.columns(2)
col1.metric("瑞利长度 Zr", f"{z_r/1000:.2f} mm")
col2.metric("远场发散角 θ", f"{(lam/(np.pi*w0))*1000:.2f} mrad")