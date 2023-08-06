# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class QueryBuilder(Component):
    """A QueryBuilder component.
QueryBuilder is an QueryBuilder component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- label (boolean | number | string | dict | list; optional): A label that will be printed when this component is rendered.
- value (boolean | number | string | dict | list; optional): The value displayed in the input.
- columns (boolean | number | string | dict | list; optional): The columns displayed in the input.
- Parameterarray (boolean | number | string | dict | list; optional): The Parameterarray displayed in the input.
- conditionArray (boolean | number | string | dict | list; optional): The conditionArray displayed in the input."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, label=Component.UNDEFINED, value=Component.UNDEFINED, columns=Component.UNDEFINED, Parameterarray=Component.UNDEFINED, conditionArray=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'label', 'value', 'columns', 'Parameterarray', 'conditionArray']
        self._type = 'QueryBuilder'
        self._namespace = 'query_builder'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'label', 'value', 'columns', 'Parameterarray', 'conditionArray']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(QueryBuilder, self).__init__(**args)
