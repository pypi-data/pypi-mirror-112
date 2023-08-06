# dynamic loading based on Dashboard code
# Version 3 dynamic loader
import os
from pathlib import Path
from importlib import import_module
from .generic_base import Instrument
import warnings

here = str(Path(__file__).resolve().parent)
directory_name = here.replace(str(Path(__file__).resolve().parent.parent), "").replace("/", "")  # gross solution
instruments = {}
for directory in os.scandir(here):
    if directory.is_dir() and not directory.name.__contains__("__"):
        modules = {}
        for file in os.listdir(directory):
            dname = str(directory.name).replace(here, "")
            if str(file).__contains__(f"{dname}_"):
                sname = str(file).replace(".py", "")
                try:
                    module = import_module(f"{directory_name}.{directory.name}.{sname}")
                    modules[module.name] = {"name": module.name, "module": module, "hwid": module.hwid}
                except Exception as ex:
                    print(f"{file} import failed")
                    print(ex)
                else:
                    instruments[module.name] = module
        globals()[directory.name] = Instrument(modules=modules, name=directory.name)
    elif directory.name.__contains__("ports"):
        globals()["ports"] = import_module(f"{directory_name}.ports")
    elif directory.name.__contains__("stellarnet"):
        globals()["stellarnet"] = import_module(f"{directory_name}.stellarnet")
    elif not directory.name.__contains__("__"):
        file = directory.name
        if not str(file).__contains__("base"):
            sname = file.replace(".py", "")
            try:
                module = import_module(f"{directory_name}.{sname}")
                try:
                    name = module.name
                    hwid = module.hwid
                    modules = {name: {"name": name, "module": module, "hwid": hwid}}
                    globals()[name] = Instrument(modules=modules, name=name)
                except:
                    name = sname
                    warnings.warn(
                        f"{sname} not properly formatted, implement name and hwid and create a class to use properly.")
                    globals()[name] = module
            except Exception as ex:
                print(f"{file} import failed")
                print(ex)
