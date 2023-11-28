import os
import sys
file_path = os.path.join(os.path.dirname(__file__), '..')
file_dir = os.path.dirname(os.path.realpath('__file__')) + "/"
sys.path.insert(0, os.path.abspath(file_path))

# este código se utiliza para asegurarse de que Python pueda encontrar los módulos que pueden estar en un
# directorio superior al directorio actual donde se está ejecutando el script. 