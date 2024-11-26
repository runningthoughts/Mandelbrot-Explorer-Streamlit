import sys
import os 
import signal

# Handles in-memory image handling instead of writing to a file
from io import BytesIO

# This replaces the Flask methods used in the standalone version
import streamlit as st

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for matplotlibz

#################################################################
# Here are all the Presets from the older JavaScript code.
# Streamlit is stateless, so have to preserve the Preload value
# in a purposeful state and then simply load those values each
# time the page loads.
#################################################################
PRESETS = [
    [-0.5, 0.0, 1.0, 200, 0],
    [-0.5, -0.605, 150.0, 200, 0],
    [-1.15, -0.275, 30.0, 200, 1],
    [-0.8, 0.181, 200.0, 200, 2],
    [0.27, -0.005, 1000.0, 200, 3],
    [-0.483, -0.625, 1000.0, 200, 4],
    [-1.04, 0.349, 800.0, 200, 5]
]

#################################################################
# Calculate the Mandelbrot set
# xmin-ymax variables define the range of the complex plane
# img variables allow mapping to an image
# Max iterations controls a sort of resolution of the final image
#################################################################
def mandelbrot_set(xmin, xmax, ymin, ymax, img_width, img_height, max_iter):
    real = np.linspace(xmin, xmax, img_width)
    imag = np.linspace(ymin, ymax, img_height)
    real, imag = np.meshgrid(real, imag)
    c = real + 1j * imag
    z = np.zeros_like(c)
    mandelbrot = np.full(c.shape, max_iter, dtype=int)

    mask = np.full(c.shape, True, dtype=bool)
    for i in range(max_iter):
        z[mask] = z[mask] ** 2 + c[mask]
        mask_new = (np.abs(z) <= 2)
        mandelbrot[mask & (~mask_new)] = i
        mask = mask & mask_new
        if not mask.any():
            break

    return mandelbrot

#################################################################
# Streamlit Page Settings
#################################################################
st.set_page_config(page_title="Mandelbrot Explorer", layout="centered")
st.title("Mandelbrot Set Explorer")
st.write("Explore the Mandelbrot Set by adjusting the parameters below.")

# Initialize session state for preset index if not already set
if 'preset_idx' not in st.session_state:
    st.session_state.preset_idx = 0

#################################################################
# Extract the Form data, then generates the Mandelbrot using the
# function above, then uses Matplotlib to plot it out, using the
# viridis colormap initially (user can change this in the webpage
#################################################################

# User inputs for generating the Mandelbrot set
preset_buttons = [st.sidebar.button(f"Preset {i+1}") for i in range(6)]
for i, button in enumerate(preset_buttons):
    if button:
        st.session_state.preset_idx = i + 1

selected_preset = PRESETS[st.session_state.preset_idx]

center_x = st.sidebar.number_input("Center X", value=selected_preset[0], format="%.5f")
center_y = st.sidebar.number_input("Center Y", value=selected_preset[1], format="%.5f")
zoom = st.sidebar.number_input("Zoom Level", min_value=0.1, value=selected_preset[2], step=0.1, format="%.2f")
max_iter = st.sidebar.slider("Max Iterations", min_value=50, max_value=1000, value=selected_preset[3])
color_map = st.sidebar.selectbox("Color Map", ["viridis", "inferno", "seismic", "BrBG", "twilight", "nipy_spectral"], index=selected_preset[4])

# # User inputs for generating the Mandelbrot set
# center_x = st.sidebar.number_input("Center X", value=-0.5, format="%.5f")
# center_y = st.sidebar.number_input("Center Y", value=0.0, format="%.5f")
# zoom = st.sidebar.number_input("Zoom Level", min_value=0.1, value=1.0, step=0.1, format="%.2f")
# max_iter = st.sidebar.slider("Max Iterations", min_value=50, max_value=1000, value=200)
# color_map = st.sidebar.selectbox("Color Map", ["viridis", "inferno", "seismic", "BrBG", "twilight", "nipy_spectral"])

cols = st.columns(6, gap="small")
cols[0].image("static/p1.png", caption="Preset 1")
cols[1].image("static/p2.png", caption="Preset 2")
cols[2].image("static/p3.png", caption="Preset 3")
cols[3].image("static/p4.png", caption="Preset 4")
cols[4].image("static/p5.png", caption="Preset 5")
cols[5].image("static/p6.png", caption="Preset 6")

# bcols = st.columns(6)
# if bcols[0].button("Preset 1"):
#     center_x.value=-0.5
#     center_y.value=-0.605
#     zoom.value=150
#     color_map.value="viridis"

# bcols[1].button("Preset 2")
# bcols[2].button("Preset 3")
# bcols[3].button("Preset 4")
# bcols[4].button("Preset 5")
# bcols[5].button("Preset 6")

# Button to generate Mandelbrot set
if st.sidebar.button("Generate Mandelbrot Set"):
    st.write("Generating Mandelbrot Set...")

    img_width, img_height = 1200, 1200
    zoom_factor = 1 / zoom
    xmin = center_x - zoom_factor
    xmax = center_x + zoom_factor
    ymin = center_y - zoom_factor
    ymax = center_y + zoom_factor

    # Generate the fractal image
    mandelbrot_image = mandelbrot_set(
        xmin, xmax, ymin, ymax, img_width, img_height, max_iter
    )

    # Plot the fractal
    plt.figure(figsize=(6, 6), dpi=220)
    plt.imshow(
        mandelbrot_image,
        extent=(xmin, xmax, ymin, ymax),
        cmap=color_map,
        interpolation='bilinear'
    )
    plt.axis('off')

    # Save the plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    buf.seek(0)


    # Display the generated Mandelbrot set
    st.image(buf, caption="Mandelbrot Set", use_column_width=True)
