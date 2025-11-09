"""Navi – Neuro-Adaptive Copilot core package."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("navi")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

__all__ = ["__version__"]

