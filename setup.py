import cx_Freeze
import sys
import os

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executaveis = [cx_Freeze.Executable(script="main.py", base=base, icon="recursos/assets/icone.ico")]

cx_Freeze.setup(
    name="Craque Neto",
    version="1.0",
    description="Jogo do Craque Neto",
    options={
        "build_exe": {
            "packages": ["pygame", "tkinter", "pyttsx3", "speech_recognition", "threading", "time", "random", "json", "os", "math"],
            "include_files": [
                "recursos/",
                "dados.json",  # se o jogo já usa um arquivo de dados
                "log.dat"      # se já existe o arquivo log
            ]
        }
    },
    executables=executaveis
)
