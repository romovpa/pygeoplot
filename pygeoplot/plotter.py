"""
Map plotter interface.
"""

from display import display_map, map_to_html

class Map(object):
    """
    Representation of map with data plotted.
    """

    def __init__(self, width=640, height=480, resizeable=False,
                 center=[55.76, 37.64], zoom=12):
        self.width = width
        self.height = height
        self.resizeable = resizeable
        self.placemarks = []
        self.center = center
        self.zoom = zoom
        self.heatmap = None

    def add_placemark(self, lat, lng, description):
        self.placemarks.append({
            'geometry': [lat, lng],
            'properties': {'balloonContent': description},
        })

    def set_heatmap(self, data):
        self.heatmap = data

    def to_dict(self):
        return {
            'container': {
                'width': self.width,
                'height': self.height,
                'resizeable': self.resizeable,
            },
            'viewport': {
                'center': self.center,
                'zoom': self.zoom,
            },
            'placemarks': self.placemarks,
            'heatmap': self.heatmap,
        }

    def display(self):
        display_map(self)

    def save_html(self, file):
        file.write(map_to_html(self))
