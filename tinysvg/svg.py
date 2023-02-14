import jinja2
from .style import Style

TEMPLATE = '''{{header}}
{%- for i in drawing %}
    {{i}}
{%- endfor %}
{{footer}}
'''

DOCTYPE = '''<?xml version="1.0"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">

'''


def create_arg(name, value, unit=''):
    name = name.replace('_', '-')
    return f'{name}="{value}{unit}"' if value is not None else ''


def create_args(**kwargs):
    res = ' '.join([ create_arg(name, value) for name, value in kwargs.items()])
    return ' ' + res if res else ''

def generic_tag(name, embed=None, **kwargs):
    embed_list = '\n'.join(embed) if embed else ''
    args = create_args(**kwargs)

    if embed:
        return f'''<{name}{args}>
{embed_list}
</{name}>
'''
    else:
        return f'<{name}{args} />'


class SVGError(BaseException):
    def __init__(self, message):
        super().__init__(self, message)


class SVG:
    def __init__(self, width, height, viewport=(0, 0, 1000, 1000), inline=True):
        self.width = width
        self.height = height
        self.viewport = viewport
        self.inline = inline
        self.style = Style()
        self.drawing = []

    def __str__(self):
        return jinja2.Environment().from_string(TEMPLATE).render(
            header=self._header(),
            drawing=self.drawing,
            footer=self._footer(),
        )

    def _header(self):
        dt = '' if self.inline else DOCTYPE

        return f'''{dt}<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{self.width}" height="{self.height}"
     viewPort="0 0 1000 1000">
'''

    def _footer(self):
        return '</svg>'

    def save(self, fname):
        with open(fname, 'w') as f:
            print(self, file=f)

    def add(self, item):
        self.drawing.append(item)

    def _style_or_not(self, style):
        s = str(self.style)
        return { 'style': s } if style and s else {}

    def stop(self, **kwargs):
        return generic_tag('stop', **kwargs)

    def linear_gradient(self, id, stops, **kwargs):
        return generic_tag('linearGradient', id=id, embed=stops, **kwargs)

    def radial_gradient(self, id, stops, cx=50, cy=50, fx=50, fy=50, fr=0, r=50, spread_method="pad"):
        stop_list = '\n'.join(stops)
        return f'''<radialGradient id="{id}" cx="{cx}%" cy="{cy}%" fx="{fx}%" fy="{fy}%" fr="{fr}%" r="{r}%" spreadMethod="{spread_method}">
{stop_list}
</radialGradient>
'''

    def pattern(self, id, patterns, **kwargs):
        return generic_tag('pattern', id=id, embed=patterns, **kwargs)

    def symbol(self, id, drawing, **kwargs):
        return generic_tag('symbol', id=id, embed=drawing, **kwargs)

    def defs(self, embed, **kwargs):
        return generic_tag('defs', embed=embed, **kwargs)

    def translate(self, x, y):
        return f'translate({x}, {y})'

    def scale(self, s):
        return f'scale({s})'

    def rotate(self, degrees, x, y):
        return f'rotate({degrees}, {x}, {y})'

    def skewx(self, degrees):
        return f'skewX({degrees})'

    def skewy(self, degrees):
        return f'skewY({degrees})'

    def transform(self, transformations, **kwargs):
        return ' '.join(transformations)

    def rect(self, style=True, **kwargs):
        kwargs.update(self._style_or_not(style))

        return generic_tag('rect', **kwargs)

    def circle(self, style=True, **kwargs):
        kwargs.update(self._style_or_not(style))

        return generic_tag('circle', **kwargs)

    def ellipse(self, style=True, **kwargs):
        kwargs.update(self._style_or_not(style))

        return generic_tag('ellipse', **kwargs)

    def line(self, x1, y1, x2, y2, style=True, **kwargs):
        kwargs.update(self._style_or_not(style))

        return generic_tag('line', x1=x1, y1=y1, x2=x2, y2=y2, **kwargs)

    def polyline(self, points, style=True, **kwargs):
        kwargs.update(self._style_or_not(style))

        point = lambda x, y: f'{x},{y}'
        points_arg = ' '.join([ point(x, y) for x, y in points ])

        return generic_tag('polyline', points=points_arg, **kwargs)

    def path(self, steps, style=True, **kwargs):
        kwargs.update(self._style_or_not(style))

        d_arg = ' '.join([ str(step) for step in steps ])

        return generic_tag('path', d=d_arg, **kwargs)

    def image(self, **kwargs):
        if 'xlink_href' in kwargs:
            kwargs['xlink:href'] = kwargs.pop('xlink_href')

        return generic_tag('image', **kwargs)

    def text_anchor(self, anchor):
        if anchor not in ['start', 'middle', 'end']:
            raise SVGError(f'"{anchor}" is not a legal text-anchor')
        return anchor

    def baseline_shift(self, baseline):
        if baseline not in ['super', 'sub', 'baseline']:
            raise SVGError(f'"{baseline}" is not a legal baseline-shift')

    def text(self, text, **kwargs):
        return generic_tag('text', embed=text, **kwargs)

    def tspan(self, text, **kwargs):
        return generic_tag('text', embed=text, **kwargs)

    def g(self, embed, **kwargs):
        return generic_tag('g', embed=embed, **kwargs)

