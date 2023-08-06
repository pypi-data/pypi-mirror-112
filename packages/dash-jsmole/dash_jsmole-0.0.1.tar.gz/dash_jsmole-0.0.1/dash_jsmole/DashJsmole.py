# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashJsmole(Component):
    """A DashJsmole component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- actionCode (number; optional):
    set  action code for menu.

- atomClick (number; optional):
    The atom clicked of component.

- atomHover (number; optional):
    The highlighted Atom.

- atomsMark (string; default ''):
    The atoms marked string atom,color.

- bondClick (number; optional):
    The bond clicked of component.

- bondHover (number; optional):
    The highlighted bond.

- bondsMark (string; default ''):
    The bonds marked string bond,color.

- height (string; default '400px'):
    The height of rendered componenet.

- jmeEvent (dict; optional):
    jsmeEvent information.

- lineWidth (number; default 1.5):
    The line width of component.

- options (string; optional):
    The options for rendered component.

- smiles (string; default ''):
    The smiles string of component.

- src (string; optional):
    The source url for jsme.nocache.js.

- width (string; default '400px'):
    The width of rendered compnent."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, height=Component.UNDEFINED, width=Component.UNDEFINED, options=Component.UNDEFINED, smiles=Component.UNDEFINED, lineWidth=Component.UNDEFINED, atomHover=Component.UNDEFINED, bondHover=Component.UNDEFINED, atomClick=Component.UNDEFINED, bondClick=Component.UNDEFINED, atomsMark=Component.UNDEFINED, bondsMark=Component.UNDEFINED, jmeEvent=Component.UNDEFINED, src=Component.UNDEFINED, actionCode=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'actionCode', 'atomClick', 'atomHover', 'atomsMark', 'bondClick', 'bondHover', 'bondsMark', 'height', 'jmeEvent', 'lineWidth', 'options', 'smiles', 'src', 'width']
        self._type = 'DashJsmole'
        self._namespace = 'dash_jsmole'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'actionCode', 'atomClick', 'atomHover', 'atomsMark', 'bondClick', 'bondHover', 'bondsMark', 'height', 'jmeEvent', 'lineWidth', 'options', 'smiles', 'src', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashJsmole, self).__init__(**args)
