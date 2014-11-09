"""
Routines for generating HTML that shows Map object.
"""

import random
import json

import jinja2
from IPython.display import display, HTML


__all__ = ['map_to_html', 'display_map']


# Simple HTML template. This works in standalone web pages for single figures,
# but will not work within the IPython notebook due to the presence of
# requirejs
SIMPLE_HTML = jinja2.Template("""
<script type="text/javascript" src="{{ d3_url }}"></script>
<script type="text/javascript" src="{{ mpld3_url }}"></script>

<style>
{{ extra_css }}
</style>

<div id={{ figid }}></div>
<script type="text/javascript">

  !function(mpld3){
       {{ extra_js }}
       mpld3.draw_figure({{ figid }}, {{ figure_json }});
  }(mpld3);


</script>
""")


# RequireJS template.  If requirejs and jquery are not defined, this will
# result in an error.  This is suitable for use within the IPython notebook.
REQUIREJS_HTML = jinja2.Template("""
<style>
{{ extra_css }}
</style>

<div id={{ figid }}></div>
<script type="text/javascript">

if(typeof(window.mpld3) !== "undefined" && window.mpld3._mpld3IsLoaded){
    !function (mpld3){
            {{ extra_js }}
            mpld3.draw_figure({{ figid }}, {{ figure_json }});
    }(mpld3);
}else{
  require.config({paths: {d3: "{{ d3_url[:-3] }}"}});
  require(["d3"], function(d3){
    window.d3 = d3;
    $.getScript("{{ mpld3_url }}", function(){
       {{ extra_js }}
       mpld3.draw_figure({{ figid }}, {{ figure_json }});
    });
  });
}
</script>
""")


# General HTML template.  This should work correctly whether or not requirejs
# is defined, and whether it's embedded in a notebook or in a standalone
# HTML page.
GENERAL_HTML = jinja2.Template("""

<style>
{{ extra_css }}
</style>

<div id={{ figid }}></div>
<script>
function mpld3_load_lib(url, callback){
  var s = document.createElement('script');
  s.src = url;
  s.async = true;
  s.onreadystatechange = s.onload = callback;
  s.onerror = function(){console.warn("failed to load library " + url);};
  document.getElementsByTagName("head")[0].appendChild(s);
}

if(typeof(mpld3) !== "undefined" && mpld3._mpld3IsLoaded){
   // already loaded: just create the figure
   !function(mpld3){
       {{ extra_js }}
       mpld3.draw_figure({{ figid }}, {{ figure_json }});
   }(mpld3);
}else if(typeof define === "function" && define.amd){
   // require.js is available: use it to load d3/mpld3
   require.config({paths: {d3: "{{ d3_url[:-3] }}"}});
   require(["d3"], function(d3){
      window.d3 = d3;
      mpld3_load_lib("{{ mpld3_url }}", function(){
         {{ extra_js }}
         mpld3.draw_figure({{ figid }}, {{ figure_json }});
      });
    });
}else{
    // require.js not available: dynamically load d3 & mpld3
    mpld3_load_lib("{{ d3_url }}", function(){
         mpld3_load_lib("{{ mpld3_url }}", function(){
                 {{ extra_js }}
                 mpld3.draw_figure({{ figid }}, {{ figure_json }});
            })
         });
}
</script>
""")

TEMPLATE_DICT = {"simple": SIMPLE_HTML,
                 "notebook": REQUIREJS_HTML,
                 "general": GENERAL_HTML}



def map_to_html(map, container_id=None):
    if container_id is None:
        container_id = 'map_' + ''.join(chr(random.randint(ord('0'), ord('9'))) for i in xrange(20))

    map_dict = map.to_dict()
    params = {
        'id': container_id,
        'width': map.width,
        'height': map.height,
        'map_json': json.dumps(map_dict),
    }
    html = """
        <div id="%(id)s" style="width: %(width)dpx; height: %(height)dpx"></div>

        <script type="text/javascript">
        require.config({
            paths: {
                'ymaps': "http://api-maps.yandex.ru/2.1/?lang=ru_RU",
                'Heatmap': "https://dl.dropboxusercontent.com/u/20300574/Heatmap.min",
            }
        });

        require(['ymaps', 'Heatmap'], function() {

            config = %(map_json)s;
            ymaps.ready(init);

            var myMap;

            function init(){
                myMap = new ymaps.Map("%(id)s", {
                    center: config.viewport.center,
                    zoom: config.viewport.zoom,
                });


                config.placemarks.forEach(
                    function(entry) {
                        var placemark = new ymaps.Placemark(entry.geometry, entry.properties);
                        myMap.geoObjects.add(placemark);
                    }
                );

                if (config.heatmap != null) {
                    ymaps.modules.require(['Heatmap'], function (Heatmap) {
                        var heatmap = new Heatmap(config.heatmap);
                        heatmap.setMap(myMap);
                    });
                }
            }

            if (config.container.resizeable) {
                $(function() {
                    $("#%(id)s").resizable();
                    $("#%(id)s").on("resize", function() { myMap.container.fitToViewport(); })
                });
            }

        });
    </script>
    """ % params
    return html


def display_map(map):
    html = map_to_html(map)
    display(HTML(html))

