# para lanzarlo desde PyCharm abrir las propiedades del lanzador arriba a la derecha e incluir como parametro build

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "includes": ["queue"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

setup(  name = "IRPF_eToro_2020",
        version = "1.1",
        description = "Calculo del IRPF de Etoro",
        options = {"build_exe": build_exe_options},
        executables = [Executable("app/irpf.py", base=base)])