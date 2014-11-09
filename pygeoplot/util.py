import pandas

from .api import Map, GeoPoint

__all__ = ['placemarks_from_df']

def placemarks_from_df(geomap, df, lat_col, lng_col, index_hint=True, row_content=True):
    assert isinstance(geomap, Map)
    assert isinstance(df, pandas.DataFrame)

    def html_description(row):
        return (
            '<table>' +
            ''.join('<tr><td><b>%s</b></td><td>%s</td></tr>' % (str(key), str(value)) for key, value in row.iteritems()) +
            '</table>'
        )

    for index, row in df.iterrows():
        point = [row[lat_col], row[lng_col]]
        geomap.add_placemark(point,
            hint=str(index) if index_hint else None,
            content=html_description(row) if row_content else None,
        )

