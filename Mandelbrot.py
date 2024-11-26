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

# Allows Ctrl-C to work in PC environment
# def signal_handler(signal, frame):
#     print('You pressed Ctrl+C!')
#     sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)

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
st.set_page_config(page_title="Mandelbrot Explorer", layout="wide")
st.title("Mandelbrot Set Explorer")
st.write("Explore the Mandelbrot Set by adjusting the parameters below.")

#################################################################
# Extract the Form data, then generates the Mandelbrot using the
# function above, then uses Matplotlib to plot it out, using the
# viridis colormap initially (user can change this in the webpage
#################################################################

# User inputs for generating the Mandelbrot set
center_x = st.sidebar.number_input("Center X", value=-0.5, format="%.5f")
center_y = st.sidebar.number_input("Center Y", value=0.0, format="%.5f")
zoom = st.sidebar.number_input("Zoom Level", min_value=0.1, value=1.0, step=0.1, format="%.2f")
max_iter = st.sidebar.slider("Max Iterations", min_value=50, max_value=1000, value=200)
color_map = st.sidebar.selectbox("Color Map", ["viridis", "plasma", "inferno", "magma", "cividis", "jet"])

cols = st.columns(6, gap="small")
cols[0].image("static/p1.png", width="150")
cols[1].image("static/p2.png")
cols[2].image("static/p3.png")
cols[3].image("static/p4.png")
cols[4].image("static/p5.png")
cols[5].image("static/p6.png")

cols = st.columns(6)
cols[0].button("Preset 1")

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
