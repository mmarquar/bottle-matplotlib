'''
Bottle-matplotlinb is a plugin that integrates matplotlib with your Bottle
application. It automatically generates a mime type (png, svg, pdf) response 
for the request.

To automatically detect routes that need matplotlib figures, the plugin
searches for route callbacks that require a `fig` keyword argument
(configurable) and skips routes that do not. This removes any overhead for
routes that don't need a database connection.

`bottle.request.query.canvas_format` controls the mime type 



Usage Example::

    import bottle
    import bottle.ext.matplotlib

    app = bottle.Bottle()
    plugin = bottle.ext.matplotlib.Plugin()
    app.install(plugin)

    @app.route('/plot/<npoints:int>')
    def plot(npoints, fig):
        ax = fig.add_subplot(111)
        ax.plot(range(npoints))
        
    #route based configuration
    @app.route('/plot/<npoints:int>', matplotlib={'figsize=(4,3)'})
    def plot_smaller(npoints, fig):
        ax = fig.add_subplot(111)
        ax.plot(range(npoints))
        
'''

__author__ = "Malte Marquarding"
__version__ = '0.1.0'
__license__ = 'MIT'

import StringIO

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import inspect
from bottle import HTTPResponse, HTTPError, response, request

MIME_MAP = { 'pdf': 'application/pdf', 'png': 'image/png',
             'svg': 'image/svg+xml'}

class MatplotlibPlugin(object):
    name = 'matplotlib'

    def __init__(self, keyword='fig'):
         self.keyword = keyword
         self.figsize = None

    def setup(self, app):
        ''' Make sure that other installed plugins don't affect the same
            keyword argument.'''
        for other in app.plugins:
            if not isinstance(other, MatplotlibPlugin): continue
            if other.keyword == self.keyword:
                raise PluginError("Found another matplotlib plugin with "\
                "conflicting settings (non-unique keyword).")

    def apply(self, callback, context):
        # Override global configuration with route-specific values.
        conf = context['config'].get('matplotlib') or {}
        keyword = conf.get('keyword', self.keyword)
        figsize = conf.get('figsize', self.figsize)

        # Test if the original callback accepts a 'db' keyword.
        # Ignore it if it does not need a database handle.
        args = inspect.getargspec(context['callback'])[0]
        if keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            # Connect to the database
            fig = Figure(figsize=figsize)
            # Add the connection handle as a keyword argument.
            kwargs[keyword] = fig
            rv = callback(*args, **kwargs)
            canvas = FigureCanvas(fig)
            output = StringIO.StringIO()
            itype = 'png'
            if request.query.canvas_format \
                    and request.query.canvas_format in MIME_MAP.keys():
                itype = request.query.canvas_format
            canvas.print_figure(output, format=itype)
            response.content_type = MIME_MAP[itype]
            return output.getvalue()

        # Replace the route callback with the wrapped one.
        return wrapper

Plugin = MatplotlibPlugin
