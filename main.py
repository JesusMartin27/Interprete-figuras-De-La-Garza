import inspect
import math
import os
import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import http.server
import socketserver
import threading
import webbrowser
import sys
import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

httpd = None
server_started = False

# Configuración de logging para el servidor.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('http.server')
# Esto dirige los logs del servidor HTTP a un archivo en lugar de la consola.
logger.addHandler(logging.FileHandler(filename='http_server.log'))
class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, formato, *args):
        logger.info("%s - - [%s] %s\n" % (
            self.address_string(),
            self.log_date_time_string(),
            formato % args))

def run_server():
    global server_started
    global httpd
    PORT = int(os.environ.get('PORT', 8082))
    Handler = ServerHandler
    socketserver.TCPServer.allow_reuse_address = True
     # Esto permitirá que el servidor reutilice la dirección
    socketserver.TCPServer.allow_reuse_address = True

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
             print("Servidor HTTP corriendo en el puerto: {PORT}", file=sys.stderr)
             server_started = True
             httpd.serve_forever()
    except OSError as e:
        logger.error(str(e))
    finally:
        if server_started and httpd:
            httpd.shutdown()
            httpd.server_close()
            server_started = False
            print(f"Servidor HTTP detenido en el puerto: {PORT}", 
file=sys.stderr)

TOKENS = [
    ('START', r'^calcular area de\s+'),
    ('SHAPE', r'(cuadrado|circulo|pentagono|rectangulo|triangulo)'),
    ('NUMBER', r'\s*\d+(\.\d+)?'),
]
def tokenize(input_text):
    tokens = []
    position = 0
    while position < len(input_text):
        match = None
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(input_text, position)
            if match:
                tokens.append((token_type, match.group(0)))
                position = match.end()
                break
# Si no coincidió ningún patrón, se imprime la parte del texto que causó el problema.
        if not match:
            wrong_input = input_text[position:]
            raise SyntaxError(f'Error lexico en la entrada: "{wrong_input}" en la posición {position}.')
    return tokens
def parse_shape(tokens):
    if tokens and tokens[0][0] == 'SHAPE':
        return tokens[0][1]
    else:
        raise ValueError('Figura invalida')
def parse_measure(tokens):
    if tokens and tokens[0][0] == 'NUMBER':
        return float(tokens[0][1])
    else:
        raise ValueError('Medida invalida')
def parse_command(tokens):
    if tokens[0][0] == 'START':
        shape = parse_shape(tokens[1:]) 
        measures_tokens = tokens[2:] # Aquí posiblemente existe un desfase en los índices
        measures = [parse_measure([token]) for token in measures_tokens if token[0] == 'NUMBER']
        return shape.strip(), measures
    else:
        raise ValueError('Comando invalido')

def calc_dibj_area(shape, measures):
        dpi = 300
        cm_to_inches = 1/ 2.54
        area = calculate_area(shape, measures)
        fig_width = max(measures) * cm_to_inches
        fig_height = max(measures) * cm_to_inches

        fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)
        print(f"El área del {shape} es {area}")
        # Comienza el bloque de código de visualización
        if shape == 'cuadrado':
            lado = measures[0]
            rect = patches.Rectangle((0, 0), lado, lado, linewidth=1, edgecolor='r', facecolor='blue')
            ax.add_patch(rect)
            ax.set_xlim([0, lado])
            ax.set_ylim([0, lado])
            ax.set_aspect('equal', adjustable='datalim')
            ax.autoscale_view()
            plt.title(f'Cuadrado con lado {lado} y área {area}',fontsize=20)
            plt.savefig('grafico.png', dpi= dpi, bbox_inches='tight')
            plt.close(fig)
            plt.grid(True)
        # Se pueden añadir más condiciones para otros tipos de figuras aquí
        elif shape == 'circulo':
            radio = measures[0]
            circ = patches.Circle((radio, radio), radio, linewidth=1, edgecolor='r', facecolor='blue')
            ax.add_patch(circ)
            ax.set_xlim([0, radio * 2])
            ax.set_ylim([0, radio * 2])
            ax.set_aspect('equal', adjustable='datalim')
            ax.autoscale_view()
            plt.title(f'Círculo con radio {radio} y área {area:.2f}', fontsize=20)
            plt.savefig('grafico.png', dpi= dpi, bbox_inches='tight')
            plt.close(fig)
        elif shape == 'pentagono':
              lado = measures[0]
              poli = patches.RegularPolygon((lado, lado), numVertices=5, radius=lado / (2 * math.tan(math.pi / 5)), orientation=math.pi, linewidth=1, edgecolor='r', facecolor='blue')
              ax.add_patch(poli)
              ax.set_xlim([0, lado * 2])
              ax.set_ylim([0, lado * 2])
              ax.set_aspect('equal', adjustable='datalim')
              ax.autoscale_view()
              plt.title(f'Pentágono con lado {lado} y área {area:.2f}', fontsize=20)
              plt.savefig('grafico.png', dpi= dpi, bbox_inches='tight')
              plt.close(fig)
        elif shape == 'rectangulo':
              base = measures[0]
              altura = measures[1]
              rect = patches.Rectangle((0, 0), base, altura, linewidth=1, edgecolor='r', facecolor='blue')
              ax.add_patch(rect)
              ax.set_xlim([0, base])
              ax.set_ylim([0, altura])
              ax.set_aspect('equal', adjustable='datalim')
              ax.autoscale_view()
              plt.title(f'Rectángulo con base {base} y altura {altura} y área {area:.2f}', fontsize=20)
              plt.savefig('grafico.png', dpi= dpi, bbox_inches='tight')
              plt.close(fig)
        elif shape == 'triangulo':
              base = measures[0]
              altura = measures[1]
              triang = patches.Polygon([[0, 0], [base, 0], [base / 2, altura]], closed=True, linewidth=1, edgecolor='r', facecolor='blue')
              ax.add_patch(triang)
              ax.set_xlim([0, base])
              ax.set_ylim([0, altura])
              ax.set_aspect('equal', adjustable='box')
              ax.autoscale_view()
              plt.title(f'Triángulo con base {base} y altura {altura} y área {area:.2f}', fontsize=20)
              plt.savefig('grafico.png', dpi= dpi, bbox_inches='tight')
              plt.close(fig)
        if server_started:
         webbrowser.open('http://localhost:8000/grafico.png')
# Iniciar el servidor en un hilo separado
if not server_started:
  server_thread = threading.Thread(target=run_server)
  server_thread.daemon = True
  server_thread.start()

def calculate_area(shape, measures):
    figuras = {
        'cuadrado': lambda m: m[0] ** 2,
        'circulo': lambda m: math.pi * (m[0] ** 2),
        'pentagono': lambda m: (5 * m[0] * m[0]) / (4 * math.tan(math.pi / 5)),
        'rectangulo': lambda m: m[0] * m[1],
        'triangulo': lambda m: (m[0] * m[1]) / 2,
    }

    # Un diccionario para definir la cantidad de medidas esperadas para cada figura
    medidas_esperadas = {
        'cuadrado': 1,
        'circulo': 1,
        'pentagono': 1,
        'rectangulo': 2,
        'triangulo': 2,
    }

    if shape in figuras and len(measures) == medidas_esperadas[shape]:
        return figuras[shape](measures)
    else:
        raise ValueError('Figura o medidas invalidas')
def interpret(input_text):
    tokens = tokenize(input_text)
    shape, measures = parse_command(tokens)
    area = calculate_area(shape, measures)
    return f"El area del {shape} es {area}"
def clear_screen():

    os.system('cls' if os.name == 'nt' else 'clear')



class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Áreas")

        # Variables
        self.selec_fig = tk.StringVar()
        self.ent_semantica = tk.StringVar()
        self.result_label_var = tk.StringVar()

        # Sección 1: Selección de figura
        shape_frame = ttk.LabelFrame(root, text="1. Seleccione la Figura:")
        shape_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        shapes = ['cuadrado', 'circulo', 'pentagono', 'rectangulo', 'triangulo']
        shape_combobox = ttk.Combobox(shape_frame, values=shapes, textvariable=self.selec_fig, state="readonly")
        shape_combobox.grid(row=0, column=0, padx=10, pady=5)
        shape_combobox.set("Seleccionar Figura")

        # Sección 2: Entrada Semántica
        semantic_frame = ttk.LabelFrame(root, text="2. Ingrese la instrucción completa:")
        semantic_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        semantic_entry = ttk.Entry(semantic_frame, textvariable=self.ent_semantica)
        semantic_entry.grid(row=0, column=0, padx=10, pady=5, ipadx=20)
        semantic_entry.insert(0, "calcular area de ...")

        # Sección 3: Resultados y Errores
        result_frame = ttk.LabelFrame(root, text="3. Resultados y Errores:")
        result_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        result_label = ttk.Label(result_frame, textvariable=self.result_label_var, wraplength=400)
        result_label.grid(row=0, column=0, padx=10, pady=5)

        # Sección 4: Botón Calcular
        calculate_button = ttk.Button(root, text="Calcular", command=self.calcular_y_mostrar)
        calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Sección 5: Botón Salir
        exit_button = ttk.Button(root, text="Salir", command=self.exit_application)
        exit_button.grid(row=5, column=0, columnspan=5, pady=10)

    def exit_application(self):
            # Detener el servidor si está en ejecución
            if server_started and httpd:
                httpd.shutdown()
                httpd.server_close()

            # Cerrar la aplicación
            self.root.destroy()

    def calcular_y_mostrar(self):
        input_text = self.ent_semantica.get().strip().lower()
        selected_fig_text = self.selec_fig.get().lower()
        try:
            if not input_text.startswith('calcular area de'):
                raise ValueError('Error de sintaxis. Asegúrese de incluir la instrucción completa.')
            if selected_fig_text and selected_fig_text not in input_text:
                raise ValueError('La figura seleccionada no coincide con la instrucción.')
            result = interpret(input_text)
            self.result_label_var.set(result)
            # Generar y mostrar la imagen
            shape, measure = parse_command(tokenize(input_text))
            calc_dibj_area(shape, measure)
            # Iniciar el servidor en un hilo separado
            if not server_started:
                server_thread = threading.Thread(target=run_server)
                server_thread.daemon = True
                server_thread.start()
            # Abrir el navegador web con la imagen generada
            if server_started:
                webbrowser.open('http://localhost:8000/grafico.png')
        except SyntaxError as e:
            messagebox.showerror("Error Léxico", str(e))
        except ValueError as e:
                 messagebox.showerror("Error Semántico", str(e)) 
        except Exception as e:
            self.result_label_var.set("Ocurrió un error inesperado.")  # Para cualquier otro error

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()