import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 0. 页面配置 ---
st.set_page_config(
    page_title="高斯光束仿真实验室",
    layout="wide",  # 使用宽屏模式，显示更多信息
    initial_sidebar_state="expanded"
)

st.title("🔦 交互式光学实验室：高斯光束 (Gaussian Beam)")
st.markdown("""
本实验室用于直观演示基模高斯光束 ($TEM_{00}$) 的传播特性。
通过调整左侧参数，您可以实时观察**束腰半径**、**波前曲率**及**横截面光强**的变化。
""")

# --- 1. 侧边栏：参数输入 ---
with st.sidebar:
    st.header("🎛️ 参数设置")

    # 基础参数
    st.subheader("光源参数")
    lam_um = st.slider("波长 λ (μm)", 0.4, 1.55, 0.632, step=0.001, format="%.3f")
    w0 = st.slider("束腰半径 w0 (μm)", 1.0, 50.0, 10.0, step=0.5)

    # 仿真范围
    st.subheader("仿真视图")
    z_max = st.slider("最大传播距离 Z (mm)", 1.0, 100.0, 20.0)

    st.markdown("---")
    st.markdown("Designed by **Optics Lab**")

# --- 2. 物理计算 (NumPy) ---
# 单位换算：全部统一运算单位为微米 (um)
z_max_um = z_max * 1000
z_axis = np.linspace(-z_max_um, z_max_um, 600)

# 核心物理量计算
z_r = (np.pi * w0 ** 2) / lam_um  # 瑞利长度
theta_div = lam_um / (np.pi * w0)  # 远场发散角 (弧度)
w_z = w0 * np.sqrt(1 + (z_axis / z_r) ** 2)  # 束宽随 z 变化
R_z = z_axis * (1 + (z_r / (z_axis + 1e-9)) ** 2)  # 曲率半径 (加微小量防止除0)

# --- 3. 布局：核心可视化 ---
# 使用两列布局：左边是传播图，右边是横截面图
row1_col1, row1_col2 = st.columns([1.5, 1])

with row1_col1:
    st.subheader("1. 光束传播轮廓 (XZ 平面)")
    fig1, ax1 = plt.subplots(figsize=(8, 5))

    # 绘制束宽包络
    ax1.plot(z_axis / 1000, w_z, 'b', linewidth=2, label=r'Beam Radius $w(z)$')
    ax1.plot(z_axis / 1000, -w_z, 'b', linewidth=2)

    # 填充光强区域
    ax1.fill_between(z_axis / 1000, w_z, -w_z, color='blue', alpha=0.1, label='Beam Region')

    # 标记瑞利长度位置
    ax1.axvline(x=z_r / 1000, color='r', linestyle='--', alpha=0.5, label=r'Rayleigh Range $z_R$')
    ax1.axvline(x=-z_r / 1000, color='r', linestyle='--', alpha=0.5)

    # 装饰
    ax1.set_xlabel("Propagation Distance Z (mm)")
    ax1.set_ylabel("Radial Position r (μm)")
    ax1.set_title(f"Beam Propagation (λ={lam_um}μm, $w_0$={w0}μm)")
    ax1.legend(loc='upper right')
    ax1.grid(True, linestyle=':', alpha=0.6)

    st.pyplot(fig1)

with row1_col2:
    st.subheader("2. 横截面光强分布 (XY 平面)")

    # 增加一个滑块，让用户选择看哪个位置的横截面
    z_slice_mm = st.slider("选择观察位置 Z (mm)", -z_max, z_max, 0.0, step=0.1)
    z_slice_um = z_slice_mm * 1000

    # 计算该位置的束宽
    w_at_slice = w0 * np.sqrt(1 + (z_slice_um / z_r) ** 2)

    # 绘制该位置的横向光强分布 I(r) = I0 * exp(-2r^2/w^2)
    r_axis = np.linspace(-3 * w_at_slice, 3 * w_at_slice, 200)
    intensity = np.exp(-2 * r_axis ** 2 / w_at_slice ** 2)

    fig2, ax2 = plt.subplots(figsize=(5, 4))
    ax2.plot(r_axis, intensity, 'r-', linewidth=2)
    ax2.fill_between(r_axis, intensity, color='red', alpha=0.2)

    ax2.set_xlabel("Radial Position r (μm)")
    ax2.set_ylabel("Normalized Intensity")
    ax2.set_title(f"Intensity Profile at Z = {z_slice_mm} mm")
    ax2.set_ylim(0, 1.1)
    ax2.grid(True)

    st.pyplot(fig2)
    st.info(f"当前位置束宽 w(z): **{w_at_slice:.2f} μm**")

# --- 4. 理论与数据面板 (使用 Tabs 分页) ---
st.markdown("---")
st.subheader("📚 物理参数详解")

tab1, tab2, tab3 = st.tabs(["📐 关键参数计算", "🧮 核心公式一览", "📉 曲率半径 R(z)"])

with tab1:
    st.markdown("根据当前设置计算得出的实时参数：")

    # 使用 LaTeX + Metric 展示
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(r"**瑞利长度 (Rayleigh Range)**")
        st.latex(r"z_R = \frac{\pi w_0^2}{\lambda}")
        st.metric("计算结果 $z_R$", f"{z_r / 1000:.4f} mm", help="光束横截面积增加一倍的距离")

    with c2:
        st.markdown(r"**远场发散角 (Divergence)**")
        st.latex(r"\theta = \frac{\lambda}{\pi w_0}")
        st.metric("计算结果 $\\theta$", f"{theta_div * 1000:.2f} mrad", help="远场光束发散的半角")

    with c3:
        st.markdown(r"**共焦参数 (Confocal Parameter)**")
        st.latex(r"b = 2 z_R")
        st.metric("计算结果 $b$", f"{2 * z_r / 1000:.4f} mm", help="焦深 (Depth of Focus)")

with tab2:
    st.markdown("### 高斯光束核心方程")
    st.markdown("基模高斯光束的电场分布描述为：")
    st.latex(r"""
    E(r, z) = E_0 \frac{w_0}{w(z)} \exp\left( \frac{-r^2}{w(z)^2} \right) \exp\left( -i \left( kz + k \frac{r^2}{2R(z)} - \psi(z) \right) \right)
    """)

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("**1. 束宽变化 w(z)**")
        st.latex(r"w(z) = w_0 \sqrt{1 + \left(\frac{z}{z_R}\right)^2}")
    with col_f2:
        st.markdown("**2. 曲率半径 R(z)**")
        st.latex(r"R(z) = z \left[ 1 + \left(\frac{z_R}{z}\right)^2 \right]")

with tab3:
    st.markdown("### 波前曲率半径的变化")
    st.markdown("观察 $R(z)$ 随传播距离的变化。注意在 $z=0$ (束腰) 处，$R \to \infty$ (平面波)。")

    fig3, ax3 = plt.subplots(figsize=(10, 3))
    # 过滤掉 z=0 附近的极大值以便绘图
    mask = (np.abs(z_axis) > 0.1 * z_r)
    ax3.plot(z_axis[mask] / 1000, R_z[mask] / 1000, 'g--', label=r'Radius of Curvature $R(z)$')

    ax3.set_xlabel("Z (mm)")
    ax3.set_ylabel("R(z) (mm)")
    ax3.set_ylim(-100, 100)  # 限制Y轴范围以免由无穷大导致图表压缩
    ax3.grid(True)
    ax3.legend()
    st.pyplot(fig3)