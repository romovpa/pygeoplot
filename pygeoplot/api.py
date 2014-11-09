"""
Convenience methods for plotting data on the map.
"""

import pandas


def placemarks(data_frame, map, lat_col, lng_col):
    assert isinstance(data_frame, pandas.DataFrame)

    for idx, row in data_frame.iterrows():
        html_description = (
            '<table>' +
            ''.join('<tr><td><b>%s</b></td><td>%s</td></tr>' % (str(key), str(value)) for key, value in row.iteritems()) +
            '</table>'
        )
        map.add_placemark(lat=row[lat_col], lng=row[lng_col], description=html_description)

def heatmap(data_frame, map, lat_col, lng_col):
    assert isinstance(data_frame, pandas.DataFrame)
    heatmap_data = zip(data_frame.ix[:, lat_col].values, data_frame.ix[:, lng_col].values)
    map.set_heatmap(heatmap_data)