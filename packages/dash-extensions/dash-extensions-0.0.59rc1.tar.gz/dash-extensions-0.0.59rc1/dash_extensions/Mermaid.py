# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Mermaid(Component):
    """A Mermaid component.
A light wrapper of https://github.com/e-attestations/react-mermaid2.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- chart (string; optional): The mermaid code of your chart. Check Mermaid js documentation for details
- name (string; optional): On optional name of your mermaid diagram/flowchart/gantt etc.
- config (dict; optional): On optional object with one of several Mermaid config parameters. Check Mermaid js documentation for details
- id (string; optional): The ID used to identify this component in Dash callbacks
- className (string; optional): The class of the component"""
    @_explicitize_args
    def __init__(self, children=None, chart=Component.UNDEFINED, name=Component.UNDEFINED, config=Component.UNDEFINED, id=Component.UNDEFINED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'chart', 'name', 'config', 'id', 'className']
        self._type = 'Mermaid'
        self._namespace = 'dash_extensions'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'chart', 'name', 'config', 'id', 'className']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Mermaid, self).__init__(children=children, **args)
