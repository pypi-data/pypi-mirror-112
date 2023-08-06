# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashFeatureViewer(Component):
    """A DashFeatureViewer component.
Feature Viewer for Protein or DNA sequences
From Calipho 
Add Features as object
Selected Feature or Sequence available in callback

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- options (dict; default {
    showAxis: true,
    showSequence: true,
    brushActive: true, //zoom
    toolbar: true, //current zoom & mouse position
    bubbleHelp: true, 
    zoomMax: 50 
}): Options for Feature Viewer.
- sequence (string; optional): The Sequence or integer length value.
- features (list; optional): The Features to View.
- viewerStyle (dict; default {'width': '800px'}): The Style of Viewer.
- zoom (list; optional): The Zoom of Viewer.
- selectedSeq (list; optional): The selected sequence of Viewer.
- darkMode (boolean; optional): The selected sequence of Viewer."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, options=Component.UNDEFINED, sequence=Component.UNDEFINED, features=Component.UNDEFINED, viewerStyle=Component.UNDEFINED, zoom=Component.UNDEFINED, selectedSeq=Component.UNDEFINED, darkMode=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'options', 'sequence', 'features', 'viewerStyle', 'zoom', 'selectedSeq', 'darkMode']
        self._type = 'DashFeatureViewer'
        self._namespace = 'dash_feature_viewer'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'options', 'sequence', 'features', 'viewerStyle', 'zoom', 'selectedSeq', 'darkMode']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashFeatureViewer, self).__init__(**args)
