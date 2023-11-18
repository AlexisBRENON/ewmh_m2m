# -*- coding: utf-8 -*-
import importlib.metadata

try:
    # Change here if project is renamed and does not equal the package name
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = 'unknown'
finally:
    del importlib.metadata
