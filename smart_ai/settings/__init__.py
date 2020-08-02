__author__ = "Mohit Thakkar"

try:
    from .production import *
except Exception:
    from .local import *
