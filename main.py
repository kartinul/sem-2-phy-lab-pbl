import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

st.set_page_config(page_title="Solar Cell Simulator", layout="wide")
plt.style.use("dark_background")

st.title("Solar Panel Simulation")

c1, c2 = st.columns(2)
with c1:
    light_intensity = st.slider("Light Intensity (W/m²)", 0.1, 2.0, 1.0)
with c2:
    angle_deg = st.slider("Sun Angle (Degrees)", 0, 180, 90)

theta = np.radians(angle_deg)
Voc_base, Isc_base = 0.6, 1.0
Isc = Isc_base * light_intensity * np.sin(theta)
Voc = Voc_base * (1 + 0.2 * np.log(light_intensity + 1))

V = np.linspace(0, Voc, 100)
I = Isc * (1 - V / Voc)
P = V * I
idx = np.argmax(P)
Vmp, Imp, Pmax = V[idx], I[idx], P[idx]
FF = (Vmp * Imp) / (Voc * Isc) if Voc * Isc != 0 else 0

col1, col2 = st.columns([1.6, 1])

with col1:
    st.subheader("Visual Simulation")
    fig, ax = plt.subplots(figsize=(7, 4.8), dpi=100)
    ax.set_facecolor("#000814")
    fig.patch.set_facecolor("#000814")

    cx, cy, radius = 0.5, 0.05, 0.72
    sun_x, sun_y = cx + radius * np.cos(theta), cy + radius * np.sin(theta)

    for r, alpha in zip(np.linspace(0.12, 0.04, 8), np.linspace(0.05, 0.3, 8)):
        ax.add_patch(plt.Circle((sun_x, sun_y), r, color="#FFD60A", alpha=alpha, lw=0))
    ax.add_patch(plt.Circle((sun_x, sun_y), 0.04, color="#FFC300", lw=0))
    ax.add_patch(plt.Circle((sun_x, sun_y), 0.02, color="white", lw=0))

    pw, ph = 0.4, 0.08
    px, py = cx - pw / 2, cy - ph / 2
    ax.add_patch(
        plt.Rectangle(
            (px - 0.02, py - 0.02), pw + 0.04, ph + 0.04, color="#333533", zorder=2
        )
    )
    ax.add_patch(plt.Rectangle((px, py), pw, ph, color="#003566", zorder=3))
    for i in range(1, 10):
        ax.plot(
            [px + i * pw / 10, px + i * pw / 10],
            [py, py + ph],
            color="#4CC9F0",
            linewidth=0.5,
            alpha=0.3,
            zorder=4,
        )

    if light_intensity > 0:
        for tx in np.linspace(px + 0.05, px + pw - 0.05, 7):
            for lw, a in zip([8, 4, 1.5], [0.05, 0.1, 0.3]):
                ax.plot(
                    [sun_x, tx],
                    [sun_y, cy],
                    color="#FFD60A",
                    alpha=a * (light_intensity / 1.5),
                    linewidth=lw * light_intensity,
                    zorder=1,
                )

    ax.plot(
        [cx, cx + 0.4], [cy, cy], color="white", linestyle="--", alpha=0.3, linewidth=1
    )
    ax.plot(
        [cx, sun_x],
        [cy, sun_y],
        color="#FFD60A",
        linestyle="--",
        alpha=0.3,
        linewidth=1,
    )
    ax.add_patch(
        Arc(
            (cx, cy),
            0.25,
            0.25,
            angle=0,
            theta1=0,
            theta2=angle_deg,
            color="#FFD60A",
            linewidth=2,
            alpha=0.8,
        )
    )

    t_a = np.radians(angle_deg / 2)
    ax.text(
        cx + 0.35 * np.cos(t_a),
        cy + 0.35 * np.sin(t_a),
        f"{angle_deg}°",
        color="white",
        fontsize=10,
        ha="center",
        fontweight="bold",
    )

    ax.set_xlim(-0.4, 1.4)
    ax.set_ylim(-0.1, 1.0)
    ax.axis("off")
    st.pyplot(fig, use_container_width=True)

with col2:
    st.metric("Current Power Output", f"{Pmax:.3f} W")
    st.subheader("Key Parameters")
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown("**Voc (Open Circuit)**")
        st.latex(r"V_{oc} = V_{oc,0} (1 + 0.2 \ln(I_L + 1))")
        st.info(f"{Voc:.3f} V")
    with r1c2:
        st.markdown("**Isc (Short Circuit)**")
        st.latex(r"I_{sc} = I_{sc,0} \cdot I_L \cdot \sin(\theta)")
        st.info(f"{Isc:.3f} A")
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.markdown("**Pmax (Max Power)**")
        st.latex(r"P_{max} = V_{mp} \cdot I_{mp}")
        st.success(f"{Pmax:.3f} W")
    with r2c2:
        st.markdown("**Fill Factor (FF)**")
        st.latex(r"FF = \frac{P_{max}}{V_{oc} \cdot I_{sc}}")
        st.success(f"{FF:.3f}")

st.subheader("Performance Curves")
g_c1, g_c2 = st.columns(2)
with g_c1:
    fg3, ax3 = plt.subplots(figsize=(6, 4), dpi=100)
    ax3.plot(V, I, color="#4CC9F0", linewidth=2)
    ax3.scatter(
        Vmp, Imp, color="#FF006E", zorder=5, label=f"MPP ({Vmp:.2f}V, {Imp:.2f}A)"
    )
    ax3.set_title("I-V Curve", fontsize=11)
    ax3.set_xlabel("Voltage (V)", fontsize=9)
    ax3.set_ylabel("Current (A)", fontsize=9)
    ax3.tick_params(labelsize=8)
    ax3.grid(alpha=0.2)
    ax3.legend(fontsize=8)
    st.pyplot(fg3, use_container_width=True)
with g_c2:
    fg4, ax4 = plt.subplots(figsize=(6, 4), dpi=100)
    ax4.plot(V, P, color="#FFD60A", linewidth=2)
    ax4.scatter(Vmp, Pmax, color="#FF006E", zorder=5, label=f"Pmax ({Pmax:.2f}W)")
    ax4.set_title("Power Curve", fontsize=11)
    ax4.set_xlabel("Voltage (V)", fontsize=9)
    ax4.set_ylabel("Power (W)", fontsize=9)
    ax4.tick_params(labelsize=8)
    ax4.grid(alpha=0.2)
    ax4.legend(fontsize=8)
    st.pyplot(fg4, use_container_width=True)
