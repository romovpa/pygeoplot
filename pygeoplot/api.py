"""
Map plotter interface.
"""

from IPython.display import HTML, display

from .display import map_to_html, standalone_html

__all__ = ['Map', 'GeoPoint']

class GeoPoint(object):
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    @staticmethod
    def parse(obj):
        if isinstance(obj, GeoPoint):
            return obj # FIXME: why doesnt work?
        elif (isinstance(obj, list) or isinstance(obj, tuple)) and len(obj) == 2:
            return GeoPoint(lat=obj[0], lng=obj[1])
        elif isinstance(obj, str):
            parts = obj.split(',', 1)
            return GeoPoint(lat=float(parts[0]), lng=float(parts[1]))
        else:
            raise ValueError('Cannot convert "%s" to GeoPoint' % repr(obj))

    def to_coord(self):
        return (self.lat, self.lng)


def _coordinates(point):
    return GeoPoint.parse(point).to_coord()


def _coordinates_many(points):
    return [GeoPoint.parse(point).to_coord() for point in points]


class Map(object):
    """
    Canvas for visualizing data on the interactive map.
    """

    def __init__(self):
        self.center = [55.76, 37.64]
        self.zoom = 8
        self.objects = []

    def set_state(self, center, zoom):
        self.center = center
        self.zoom = zoom

    def add_object(self, obj):
        self.objects.append(obj)

    def add_placemark(self, point, hint=None, content=None):
        self.add_object({
            'type': 'Placemark',
            'point': _coordinates(point),
            'hint': hint,
            'content': content,
        })

    def add_line(self, points, hint=None, content=None, color='#000000', width=4, opacity=0.5):
        self.add_object({
            'type': 'Line',
            'points': _coordinates_many(points),
            'hint': hint,
            'content': content,
            'color': color,
            'width': width,
            'opacity': opacity,
        })

    def add_heatmap(self, points):
        self.add_object({
            'type': 'Heatmap',
            'points': _coordinates_many(points),
        })

    def to_dict(self):
        """
        Outputs JSON-serializable dictionary representation of the map plot.
        """
        return {
            'state': {
                'center': self.center,
                'zoom': self.zoom,
            },
            'objects': self.objects,
        }

    def to_html(self, *args, **kwargs):
        return map_to_html(self, *args, **kwargs)

    def display(self, *args, **kwargs):
        display(HTML(self.to_html(*args, **kwargs)))

    def save_html(self, file, *args, **kwargs):
        if isinstance(file, str):
            with open(file, 'w') as f:
                self.save_html(f, *args, **kwargs)
        else:
            file.write(standalone_html(self.to_html(*args, **kwargs)))

