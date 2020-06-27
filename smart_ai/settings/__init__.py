try:
    from .production import *
except Exception:
    from .local import *
