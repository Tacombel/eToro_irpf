from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "includes": ["queue"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

setup(  name = "eToro_parser",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("app/irpf.py", base=base)])