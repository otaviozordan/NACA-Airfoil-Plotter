import matplotlib
matplotlib.use('Agg')  # Use o backend 'Agg' para evitar problemas de GUI

from flask import Flask, render_template, request, send_from_directory
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

app = Flask(__name__)

def naca_4_digit_airfoil(naca, n_points=100):
    m = int(naca[0]) / 100.0
    p = int(naca[1]) / 10.0
    t = int(naca[2:]) / 100.0

    x = np.linspace(0, 1, n_points)

    y_t = 5 * t * (
        0.2969 * np.sqrt(x) -
        0.1260 * x -
        0.3516 * x**2 +
        0.2843 * x**3 -
        0.1015 * x**4
    )

    y_c = np.zeros_like(x)
    dyc_dx = np.zeros_like(x)

    for i in range(n_points):
        if x[i] < p:
            y_c[i] = (m / p**2) * (2 * p * x[i] - x[i]**2)
            dyc_dx[i] = (2 * m / p**2) * (p - x[i])
        else:
            y_c[i] = (m / (1 - p)**2) * ((1 - 2 * p) + 2 * p * x[i] - x[i]**2)
            dyc_dx[i] = (2 * m / (1 - p)**2) * (p - x[i])

    theta = np.arctan(dyc_dx)

    x_u = x - y_t * np.sin(theta)
    y_u = y_c + y_t * np.cos(theta)
    x_l = x + y_t * np.sin(theta)
    y_l = y_c - y_t * np.cos(theta)

    return x, y_u, y_l, y_c, y_t, m, p, t

def plot_airfoil(naca, filename):
    x, y_u, y_l, y_c, y_t, m, p, t = naca_4_digit_airfoil(naca)

    plt.figure(figsize=(12, 6))
    plt.plot(x, y_u, 'b', label='Upper Surface', linewidth=2)
    plt.plot(x, y_l, 'r', label='Lower Surface', linewidth=2)
    plt.plot(x, np.zeros_like(x), 'k--', linewidth=1)
    plt.fill_between(x, y_u, y_l, color='lightgray', alpha=0.5)  # Adiciona uma área sombreada
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'NACA {naca} Airfoil')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

    # Salva o gráfico da linha média e distribuição de espessura
    plt.figure(figsize=(12, 6))
    plt.plot(x, y_c, 'g', label='Camber Line', linewidth=2)
    plt.plot(x, y_t, 'c', label='Thickness Distribution', linestyle='--', linewidth=2)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'NACA {naca} Airfoil Camber and Thickness')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename.replace('.png', '_details.png'))
    plt.close()

    # Salva o gráfico da distribuição de pressão (estimativa simples)
    pressure_distribution = 1 - (y_t / y_c.max())**2
    plt.figure(figsize=(12, 6))
    plt.plot(x, pressure_distribution, 'm', label='Pressure Distribution', linewidth=2)
    plt.xlabel('x')
    plt.ylabel('Pressure')
    plt.title(f'NACA {naca} Airfoil Pressure Distribution')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename.replace('.png', '_pressure.png'))
    plt.close()

    # Estimativa básica do coeficiente de sustentação
    Cl = 2 * np.pi * m  # Fórmula simplificada

    # Estimativa básica do coeficiente de arrasto
    Cd = 0.01  # Valor simplificado

    # Gráficos de polares simplificados
    angles_of_attack = np.linspace(-10, 10, 100)
    polar_Cl = 2 * np.pi * m * np.sin(np.radians(angles_of_attack))  # Simplificação
    polar_Cd = Cd * (1 + np.tan(np.radians(angles_of_attack))**2)  # Simplificação

    plt.figure(figsize=(12, 6))
    plt.plot(angles_of_attack, polar_Cl, 'b', label='Lift Coefficient (Cl)', linewidth=2)
    plt.xlabel('Angle of Attack (degrees)')
    plt.ylabel('Coefficient of Lift')
    plt.title(f'NACA {naca} Airfoil Polar Curve')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename.replace('.png', '_polar.png'))
    plt.close()

    plt.figure(figsize=(12, 6))
    plt.plot(angles_of_attack, polar_Cd, 'r', label='Drag Coefficient (Cd)', linewidth=2)
    plt.xlabel('Angle of Attack (degrees)')
    plt.ylabel('Coefficient of Drag')
    plt.title(f'NACA {naca} Airfoil Drag Polar Curve')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename.replace('.png', '_polar_drag.png'))
    plt.close()

    # Geração de relatório em PDF
    pdf_filename = filename.replace('.png', '.pdf')
    with PdfPages(pdf_filename) as pdf:
        for img in [filename, filename.replace('.png', '_details.png'), filename.replace('.png', '_pressure.png'), filename.replace('.png', '_polar.png'), filename.replace('.png', '_polar_drag.png')]:
            img_plot = plt.imread(img)
            plt.figure(figsize=(12, 6))
            plt.imshow(img_plot)
            plt.axis('off')
            pdf.savefig()
            plt.close()

    return m, p, t, Cl, Cd, os.path.basename(pdf_filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        naca_code = request.form['naca_code']
        filename = os.path.join('static', 'naca_airfoil.png')
        details_filename = filename.replace('.png', '_details.png')
        pressure_filename = filename.replace('.png', '_pressure.png')
        polar_filename = filename.replace('.png', '_polar.png')
        polar_drag_filename = filename.replace('.png', '_polar_drag.png')
        pdf_filename = filename.replace('.png', '.pdf')
        m, p, t, Cl, Cd, pdf_filename = plot_airfoil(naca_code, filename)
        return render_template('index.html', image_filename='naca_airfoil.png', details_image_filename='naca_airfoil_details.png', pressure_image_filename='naca_airfoil_pressure.png', polar_image_filename='naca_airfoil_polar.png', polar_drag_image_filename='naca_airfoil_polar_drag.png', m=m, p=p, t=t, Cl=Cl, Cd=Cd, pdf_filename=pdf_filename)
    return render_template('index.html', image_filename=None, details_image_filename=None, pressure_image_filename=None, polar_image_filename=None, polar_drag_image_filename=None, m=None, p=None, t=None, Cl=None, Cd=None, pdf_filename=None)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


if __name__ == "__main__":
    app.run(debug=True)
