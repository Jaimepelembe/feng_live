#Adicionar a Raiz ao sys.path (Executando Direto) Para que possa importar sem problemas
import sys
import os

# Adiciona a pasta raiz 'sga' ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.estudanteController import CTA


tecnico=CTA("Naruto")
tecnico.start()

tecnico.sendMessage("Ola mundo")