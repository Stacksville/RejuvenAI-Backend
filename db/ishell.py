# To interact with DB install using `pip install ipython` and run `python3 ishell.py`
# from IPython import embed
#
# from configs.database import Base
# from src.main import app  # NOQA
#
# banner = "Additional imports:\n"
#
# banner = f"{banner}from settings.main import app\n"
#
# for clzz in Base.registry._class_registry.values():
#     if hasattr(clzz, "__tablename__"):
#         globals()[clzz.__name__] = clzz
#         import_string = f"from {clzz.__module__} import {clzz.__name__}\n"
#         banner = banner + import_string
#
# embed(colors="neutral", banner2=banner)
