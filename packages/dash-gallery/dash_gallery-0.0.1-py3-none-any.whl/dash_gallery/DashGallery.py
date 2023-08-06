# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashGallery(Component):
    """A DashGallery component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- images (list; optional):
    Images to display.

- options (dict; default {lightBoxWidth: 1024, rowHeight: 100, margin: 2,          showImageCount: True, maxRows: None }):
    Gallery Options.

- selected (list; optional):
    Selected Images.

- style (dict; optional):
    Style."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, images=Component.UNDEFINED, options=Component.UNDEFINED, selected=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'images', 'options', 'selected', 'style']
        self._type = 'DashGallery'
        self._namespace = 'dash_gallery'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'images', 'options', 'selected', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashGallery, self).__init__(**args)
