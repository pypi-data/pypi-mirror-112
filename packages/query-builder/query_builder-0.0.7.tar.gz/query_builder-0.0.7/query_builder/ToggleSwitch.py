# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ToggleSwitch(Component):
    """A ToggleSwitch component.


Keyword arguments:
- id (string; required)
- checked (boolean; required)
- name (string; optional)
- optionLabels (list; default ["AND", "OR"])
- small (boolean; optional)
- disabled (boolean; optional)"""
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, checked=Component.REQUIRED, onChange=Component.REQUIRED, name=Component.UNDEFINED, optionLabels=Component.UNDEFINED, small=Component.UNDEFINED, disabled=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'checked', 'name', 'optionLabels', 'small', 'disabled']
        self._type = 'ToggleSwitch'
        self._namespace = 'query_builder'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'checked', 'name', 'optionLabels', 'small', 'disabled']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id', 'checked', 'onChange']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ToggleSwitch, self).__init__(**args)
