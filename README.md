# Mandelbrot Explorer
This is a variation of my exploration of Python, and here, pulling in math and plotting functions, Instead of using Flask to render the webpage, I am trying out Streamlit, which is a Python hosting service that provides its own framework to render the webpage.

At least for the free, "Community" free hosting, the page is a bit more basic looking. But after crawling the Streamlit documentation, I was able to add the Presets, and though the functionality is clunkier, it is an artifact of Streamlit's way of working- each button press causes the Python code to re-execute.  Therefore, you have to use a Session State variable to initialize the input values to different Presets.  It took a bit of back and forth to get this working. It's a very different way to do things, but offers the ability, rather easily, to host Python code for others to run publicly.

What is missing is the auto-scaling zoom increments, which was on the original version I released.

## Code Structure
A requirement to interface with Streamlit is to import Streamlit's libraries

### Presets
The Presets are the 6 presets that will give you interesting looking Mandelbrots to start with so you can jump around more and removes some of the initial trial and error as you get familiar with how the values will change it.

### Mandelbrot_Set
This calculates the image from the parameter sets

### Streamlit setup
Initializes the page, creates the all the Sidebar inputs, and the array of Preset thumbnails across the top

### Sidebar Buttons
When any value is changed, you must click the Generate Mandelbrot Set button.  This is also required if you click any Preset button.  Presets simply replace the values in the paramater inputs and will also clear the previous image.  Click the Generate button again to get a new image.