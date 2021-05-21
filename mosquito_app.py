# Flask application

import json
from flask import Flask
from jinja2 import Template
from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.resources import CDN
import os

app = Flask(__name__)
page = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  {{ resources }}
</head>
<body>
  <div id="myplot"></div>
  <script>
  fetch('/plot')
    .then(function(response) { return response.json(); })
    .then(function(item) { return Bokeh.embed.embed_item(item); })
  </script>
</body>
""")

@app.route('/')
def root():
    return page.render(resources=CDN.render())

@app.route('/plot')
def plot():
    import numpy as np
    from bokeh.plotting import figure, show
    from bokeh.embed import json_item
    from bokeh.models import LinearColorMapper, ColorBar, FuncTickFormatter

    # Image Import
    img = np.load('data/output.npy')
    img = np.flip(img, 0)

    # [Lat, Longs] (Upper left, Center, Bottom right) and height_width
    ul = [7.51541, 4.26682]
    br = [7.43933, 4.43152]
    dw = br[1] - ul[1]
    dh = ul[0] - br[0]
    ht_wdth_km  = [8.44, 18.16]

    # Plotting specifications
    palette = ('white','#deebf7','#9ecae1','#084594')

    TOOLS = 'wheel_zoom,pan,crosshair,hover,reset'
    cmap = LinearColorMapper(palette = palette, low=0, high=1, nan_color='red')
    p = figure(tools=TOOLS,tooltips=[("Latitude", "$y"),("Longitude", "$x")],
               plot_width=900, plot_height=450,
               match_aspect = True,
               toolbar_location="above",
               title="Gbongan, Nigeria - March 26, 2021")
    p.image(image=[img], color_mapper = cmap, x=ul[1], y=br[0], dw=dw, dh=dh)
    color_bar = ColorBar(color_mapper=cmap,label_standoff=12, border_line_color='#2F2F2F',
                         border_line_width = 8,location=(0,0))
    p.add_layout(color_bar, 'right')

    # Coloring stuff and other formatting
    p.background_fill_color = '#2F2F2F'
    p.border_fill_color = '#2F2F2F'
    p.outline_line_color = 'white'
    p.title.text_color = "white"
    p.xaxis.major_label_text_color = 'white'
    p.yaxis.major_label_text_color = "white"
    p.xaxis.axis_line_color = "white"
    p.yaxis.axis_line_color = "white"
    p.xaxis.major_tick_line_color = "white"
    p.yaxis.major_tick_line_color = "white"
    p.grid.visible = False

    # Kilometers on axis
    p.xaxis.axis_label = "Kilometers"
    p.xaxis.axis_label_text_color = "white"
    p.yaxis.formatter = FuncTickFormatter(code="""
        return (((tick - 7.43933) / (7.51541 - 7.43933)) * 8.4).toFixed(1) """)
    p.xaxis.formatter = FuncTickFormatter(code="""
        return (((tick - 4.26682) / (4.43152 - 4.26682)) * 18.16).toFixed(1) """)

    return json.dumps(json_item(p, "myplot"))

if __name__ == '__main__':
    app.run(port=5000)
