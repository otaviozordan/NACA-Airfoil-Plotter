# NACA Airfoil Plotter
#### Video Demo: https://youtu.be/ZzYQg_iRxVs

#### Description:
The NACA Airfoil Plotter is a web-based application designed to visualize and analyze NACA airfoils. This tool allows users to input a 4-digit NACA code and generates detailed plots of the corresponding airfoil, including the upper and lower surfaces, camber line, thickness distribution, pressure distribution, and polar curves for lift and drag. The application is built using Flask for the web interface and Matplotlib for plotting.

## Features
- **Input Field**: Users can enter a 4-digit NACA code to generate the corresponding airfoil profile.
- **Visualizations**: The application produces several plots:
  - Upper and lower surfaces of the airfoil.
  - Camber line and thickness distribution.
  - Pressure distribution.
  - Lift and drag polar curves.
- **PDF Report**: A downloadable PDF report containing all visualizations and analysis results.

## Technologies Used
- **Flask**: A lightweight web framework for Python, used to build the web application.
- **Matplotlib**: A comprehensive library for creating static, animated, and interactive visualizations in Python.
- **Python**: The programming language used for backend logic and data processing.

## Mathematical Formulas and Calculations

### Airfoil Geometry
The NACA 4-digit airfoil series can be characterized by three parameters: maximum camber (m), location of maximum camber (p), and maximum thickness (t).

1. **Thickness Distribution (y_t)**:
   - The thickness distribution is given by the formula:
     $
     y_t = 5 \cdot t \cdot \left(0.2969 \cdot \sqrt{x} - 0.1260 \cdot x - 0.3516 \cdot x^2 + 0.2843 \cdot x^3 - 0.1015 \cdot x^4 \right)
     $
   - Where $ t $ is the maximum thickness as a fraction of the chord length, and \( x \) is the position along the chord from 0 to 1.

2. **Camber Line (y_c) and Its Slope (dyc_dx)**:
   - For positions $ x $ less than $ p $:
     $
     y_c = \frac{m}{p^2} \cdot (2px - x^2)
     $
     $
     \frac{dy_c}{dx} = \frac{2m}{p^2} \cdot (p - x)
     $
   - For positions $ x $ greater than or equal to $ p $
     $
     y_c = \frac{m}{(1 - p)^2} \cdot \left((1 - 2p) + 2px - x^2\right)
     $
     $
     \frac{dy_c}{dx} = \frac{2m}{(1 - p)^2} \cdot (p - x)
     $
   - Where $ m $ is the maximum camber as a fraction of the chord length and $ p $ is the position of maximum camber along the chord.

3. **Angle of Attack and Surface Coordinates**:
   - The angle of attack ($ \theta $) is computed using:
     $
     \theta = \arctan \left(\frac{dy_c}{dx}\right)
     $
   - Upper and lower surface coordinates are calculated as:
     $
     x_u = x - y_t \cdot \sin(\theta)
     $
     $
     y_u = y_c + y_t \cdot \cos(\theta)
     $
     $
     x_l = x + y_t \cdot \sin(\theta)
     $
     $
     y_l = y_c - y_t \cdot \cos(\theta)
     $

### Aerodynamic Coefficients
1. **Lift Coefficient (Cl)**:
   - Simplified Lift Coefficient:
     $
     C_l = 2 \cdot \pi \cdot m
     $
   - Where $ m $ is the maximum camber of the airfoil.

2. **Drag Coefficient (Cd)**:
   - Simplified Drag Coefficient:
     $
     C_d = 0.01
     $
   - This value is a simplification and does not account for real-world variations.

3. **Polar Curves**:
   - Lift Polar Curve:
     $
     C_{l,\text{polar}} = 2 \cdot \pi \cdot m \cdot \sin(\text{angle\_of\_attack})
     $
   - Drag Polar Curve:
     $
     C_{d,\text{polar}} = C_d \cdot \left(1 + \tan(\text{angle\_of\_attack})^2\right)
     $
   - These formulas provide a simplified model of lift and drag characteristics as a function of the angle of attack.
