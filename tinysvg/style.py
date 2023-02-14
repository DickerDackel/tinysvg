class StyleError(BaseException):
    def __init__(self, message):
        super().__init__(self, message)

class Style:
    _empty = {
        'fill': None,
        'fill_rule': None,
        'fill_opacity': None,
        'stroke': None,
        'stroke_opacity': None,
        'stroke_width': None,
        'stroke_linecap': None,
        'stroke_linejoin': None,
        'stroke_miterlimit': None,
        'stroke_dasharray': None,
        'stroke_dashoffset': None,
    }

    def __init__(self, **kwargs):
        self._style = Style._empty.copy()
        self._style.update(**kwargs)

    def __str__(self):
        return ';'.join([f'{name}:{val}'
                         for name, val in self._style.items()
                         if val is not None
                         ])

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, s):
        self._style = Style._empty.copy()
        # We could simply update the dict, but we go through all setter
        # functions, since these do parameter checks
        for k, v in s.items():
            setattr(self, k, v)

    @property
    def fill(self):
        return self._style['fill']

    @fill.setter
    def fill(self, val):
        self._style['fill'] = val

    @property
    def fill_rule(self):
        return self._style['fill_rule']

    @fill_rule.setter
    def fill_rule(self, val):
        self._style['fill_rule'] = val

    @property
    def fill_opacity(self):
        return self._style['fill_opacity']

    @fill_opacity.setter
    def fill_opacity(self, val):
        self._style['fill_opacity'] = val

    @property
    def stroke(self):
        return self._style['stroke']

    @stroke.setter
    def stroke(self, val):
        self._style['stroke'] = val

    @property
    def stroke_opacity(self):
        return self._style['stroke_opacity']

    @stroke_opacity.setter
    def stroke_opacity(self, val):
        self._style['stroke_opacity'] = val

    @property
    def stroke_width(self):
        return self._style['stroke_width']

    @stroke_width.setter
    def stroke_width(self, val):
        self._style['stroke_width'] = val

    @property
    def stroke_linecap(self):
        return self._style['stroke_linecap']

    @stroke_linecap.setter
    def stroke_linecap(self, val):
        if not val in ['butt', 'round', 'square']:
            raise StyleError(f'"{val}" is not an allowed stoke-linecap')

        self._style['stroke_linecap'] = val

    @property
    def stroke_linejoin(self):
        return self._style['stroke_linejoin']

    @stroke_linejoin.setter
    def stroke_linejoin(self, val):
        self._style['stroke_linejoin'] = val

    @property
    def stroke_miterlimit(self):
        return self._style['stroke_miterlimit']

    @stroke_miterlimit.setter
    def stroke_miterlimit(self, val):
        if not val in ['miter', 'round', 'bevel']:
            raise StyleError(f'"{val}" is not an allowed stoke-miterlimit')

        self._style['stroke_miterlimit'] = val

    @property
    def stroke_dasharray(self):
        return self._style['stroke_dasharray']

    @stroke_dasharray.setter
    def stroke_dasharray(self, val):
        self._style['stroke_dasharray'] = val
    @property
    def stroke_dashoffset(self):
        return self._style['stroke_dashoffset']

    @stroke_dashoffset.setter
    def stroke_dashoffset(self, val):
        self._style['stroke_dashoffset'] = val
