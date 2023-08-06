"""Functions used to dynamically load components from Python packages
that include Dash components.
"""
import importlib

from dash.development.base_component import Component


def load_component_from_namespace(namespace: str, component_name: str) -> Component:
    try:
        package = importlib.import_module(namespace)
    except ModuleNotFoundError:
        raise AttributeError(f"Package for namespace {namespace} not found")

    if not hasattr(package, component_name):
        raise AttributeError(f"Namespace {namespace} does not contain component {component_name}")

    return getattr(package, component_name)
