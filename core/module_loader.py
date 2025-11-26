import os
import importlib

MODULES_PATH = os.path.join(os.path.dirname(__file__), "..", "modules")

def load_cve_modules():
    modules = {}

    for filename in os.listdir(MODULES_PATH):
        if not filename.endswith(".py"):
            continue
        if filename == "__init__.py":
            continue

        mod_name = filename[:-3] 
        full_import = f"modules.{mod_name}"

        try:
            module = importlib.import_module(full_import)

            if not hasattr(module, "run"):
                continue
            module_id = getattr(module, "CVE_ID", mod_name)
            modules[module_id] = module

        except Exception as e:
            print(f"[!] Failed to load module {filename}: {e}")

    return modules

