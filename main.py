import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

st.set_page_config(page_title="Solar Cell Simulator", layout="wide")
plt.style.use("dark_background")

st.title("Solar Panel Simulation")

# ---------------- CONTROLS ----------------
c1, c2, c3 = st.columns(3)
with c1:
    light_intensity = st.slider("Light Intensity (W/m²)", 0.1, 2.0, 1.0)
with c2:
    angle_deg = st.slider("Sun Angle (Degrees)", 0, 180, 90)
with c3:
    diode_factor = st.slider("Diode Factor (n)", 1.0, 2.0, 1.2)

theta = np.radians(angle_deg)

# ---------------- PHYSICS ----------------
Voc_base, Isc_base = 0.6, 1.0

# Use sin since panel is horizontal in your model
Isc = Isc_base * light_intensity * np.sin(theta)

Voc = Voc_base * (1 + 0.2 * np.log(light_intensity + 1))

V = np.linspace(0, Voc, 200)

# ---- REALISTIC CURVE (DIODE MODEL) ----
I0 = 0.01
Vt = 0.025

I = Isc - I0 * (np.exp(V / (diode_factor * Vt)) - 1)

# Avoid negative current going crazy
I = np.clip(I, 0, None)

P = V * I

idx = np.argmax(P)
Vmp, Imp, Pmax = V[idx], I[idx], P[idx]

FF = (Vmp * Imp) / (Voc * Isc) if Voc * Isc != 0 else 0

# ---------------- LAYOUT ----------------
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

    ax.plot([cx, cx + 0.4], [cy, cy], color="white", linestyle="--", alpha=0.3, linewidth=1)
    ax.plot([cx, sun_x], [cy, sun_y], color="#FFD60A", linestyle="--", alpha=0.3, linewidth=1)

    ax.add_patch(
        Arc((cx, cy), 0.25, 0.25, angle=0, theta1=0, theta2=angle_deg,
            color="#FFD60A", linewidth=2, alpha=0.8)
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
    st.subheader("Current Power")
    st.markdown(f"#### {Pmax:.3f} W")

    st.subheader("Key Parameters")

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.info(f"Voc: {Voc:.3f} V")
    with r1c2:
        st.info(f"Isc: {Isc:.3f} A")

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.success(f"Pmax: {Pmax:.3f} W")
    with r2c2:
        st.success(f"FF: {FF:.3f}")

# ---------------- GRAPHS ----------------
st.subheader("Performance Curves")

g_c1, g_c2 = st.columns(2)

with g_c1:
    fg3, ax3 = plt.subplots(figsize=(6, 4), dpi=100)
    ax3.plot(V, I, color="#4CC9F0", linewidth=2)
    ax3.scatter(Vmp, Imp, color="#FF006E", zorder=5)
    ax3.set_title("I-V Curve")
    ax3.set_xlabel("Voltage (V)")
    ax3.set_ylabel("Current (A)")
    ax3.grid(alpha=0.2)
    st.pyplot(fg3, use_container_width=True)

with g_c2:
    fg4, ax4 = plt.subplots(figsize=(6, 4), dpi=100)
    ax4.plot(V, P, color="#FFD60A", linewidth=2)
    ax4.scatter(Vmp, Pmax, color="#FF006E", zorder=5)
    ax4.set_title("Power Curve")
    ax4.set_xlabel("Voltage (V)")
    ax4.set_ylabel("Power (W)")
    ax4.grid(alpha=0.2)
    st.pyplot(fg4, use_container_width=True)