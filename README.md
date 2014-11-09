PyGeoPlot
=========

A library for plotting data on the map.

[Demo: Moscow CCTV cameras](http://nbviewer.ipython.org/github/romovpa/pygeoplot/blob/master/ipynb/DemoMoscowCCTV.ipynb)

![Teaser Image: Using PyGeoPlot in IPython Notebook](/ipynb/screen-demo-for-readme.png)

### Tutorial

#### Installing

To install PyGeoPlot just clone the repository and run `setup.py`.
```bash
$ git clone https://github.com/romovpa/pygeoplot.git
$ cd pygeoplot
$ python setup.py install
```

#### Creating map canvas

```python
import pygeoplot as gp

m = gp.Map()
```

To see empty map in your Notebook say `display()`:
```python
m.display()
```

You can specify size of the map container and even make it resizeable (by dragging the lower right corner):
```python
m.display(width=600, height=300, resizeable=True)
```

#### Drawing a line

```python
points = [
    (55.864414, 37.401979),
    (55.575286, 37.635438),
    (55.845875, 37.801606),
    (55.665433, 37.426698),
    (55.685610, 37.830446),
    (55.864414, 37.401979),
]
m.add_line(line_points, color="#FF0000", width=10, opacity=0.6)
```

#### Setting zoom and the center point

```python
center_point = (55.72, 37.64)
m.set_state(center_point, zoom=12)
```

#### Adding a placemark

```python
m.add_placemark((55.702770, 37.529184),
                hint='Alma Mater', content='Moscow State University')
m.add_placemark((55.711552, 37.621861),
                hint='The Center of the pentagram')
```

The `content` could contain any valid HTML:
```python
m.add_placemark((55.711552, 37.621861), hint='A Cat',
    content='<img width=300 height=200 src="http://www.findcatnames.com/wp-content/uploads/2014/09/453768-cats-cute.jpg" />')
```

#### Heatmap

You can visualize a set of geo-points with heatmap.
The feature is implemented by using [Yandex Maps API Heatmap Module](https://github.com/yandex/mapsapi-heatmap).

```python
points = [
    (55.864414, 37.401979),
    ...
]
m.add_heatmap(heatmap_points)
```

[Moscow CCTV cameras demo](http://nbviewer.ipython.org/github/romovpa/pygeoplot/blob/master/ipynb/DemoMoscowCCTV.ipynb)
contains an example of the heatmap of the real data.

#### Saving map to stand-alone HTML file

After completing your visualization, you could write it into stand-alone HTML file and share with colleagues.

```python
m.save_html('map_with_data.html')
```

An example of exported HTML from [Moscow CCTV cameras demo](http://nbviewer.ipython.org/github/romovpa/pygeoplot/blob/master/ipynb/DemoMoscowCCTV.ipynb):
[ipynb/demo-moscow-cctv-heatmap.html](/ipynb/demo-moscow-cctv-heatmap.html).


### Further Work

#### Todo-list
 - robust and clear javascript code base
 - drawing polygons and circles
 - changing locales


#### Wanna-list
 - supporting different map engines [Google Maps](http://maps.google.com/), [Leaflet (OSM)](http://leafletjs.com/)
