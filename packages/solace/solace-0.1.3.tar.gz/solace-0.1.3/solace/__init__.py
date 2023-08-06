import os
import json
import uuid

import logging
from logging.config import dictConfig

import munch
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.routing import Map, Rule

__version__ = '0.1.1'

apiname = os.environ.get('SOLACE_API_NAME', str(uuid.uuid4()))


DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        '': {
            'level': os.environ.get('LOG_LEVEL', 'WARNING').upper(),
        }
    }
}
logging.config.dictConfig(DEFAULT_LOGGING)

# try:
#     log_level = os.environ['LOG_LEVEL'].upper()
# except KeyError:
#     log_level = "WARNING"
#     log.warning("optional environment variable LOG_LEVEL was not set")
# log.setLevel(logging.getLevelName(log_level))
# log.warning("log level is set to {}".format(log_level))

# TODO: catch any errors that may come from not passing the proper data type here
# TODO: raise our own custom error types
def objectify(dict):
    return munch.munchify(dict)

class SolaceResponse(Response):
    json = munch.munchify({})

    def __init__(self,):
        super().__init__()

class Api:
    
    def __init__(self):
        self.rules = Map([])
        self.views = {}
    
    def __rule(self, method, urlpath, handler):
        uid = str(uuid.uuid4())
        self.rules.add(
            Rule(
                urlpath, 
                endpoint=uid,
                methods=[method]
            )
        )
        self.views[uid] = handler

    def get(self, urlpath, handler):
        """
        The GET method requests a representation of the 
        specified resource. Requests using GET should only 
        retrieve data.
        """
        self.__rule('GET', urlpath, handler)

    def head(self, urlpath, handler):
        """
        The HEAD method asks for a response identical to that
        of a GET request, but without the response body.
        """
        self.__rule('HEAD', urlpath, handler)

    def post(self, urlpath, handler):
        """
        The POST method is used to submit an entity to the 
        specified resource, often causing a change in state
        or side effects on the server.
        """
        self.__rule('POST', urlpath, handler)

    def put(self, urlpath, handler):
        """
        The PUT method replaces all current representations 
        of the target resource with the request payload.
        """
        self.__rule('PUT', urlpath, handler)

    def delete(self, urlpath, handler):
        """
        The DELETE method deletes the specified resource.
        """
        self.__rule('DELETE', urlpath, handler)

    def connect(self, urlpath, handler):
        """
        The CONNECT method establishes a tunnel to the server 
        identified by the target resource.
        """
        self.__rule('CONNECT', urlpath, handler)

    def options(self, urlpath, handler):
        """
        The OPTIONS method is used to describe the communication
        options for the target resource.
        """
        self.__rule('OPTIONS', urlpath, handler)

    def trace(self, urlpath, handler):
        """
        The TRACE method performs a message loop-back test along 
        the path to the target resource.
        """
        self.__rule('TRACE', urlpath, handler)

    def patch(self, urlpath, handler):
        """
        The PATCH method is used to apply partial modifications
        to a resource.
        """
        self.__rule('PATCH', urlpath, handler)
    
    def websocket(self, urlpath, handler):
        # NOTE: Werkzeug has no further WebSocket support beyond routing.
        # TODO: We'll need to bring in a Websocket library and support
        # events, and socket management.
        """
        """
    
    def register(self, Middleware):
        pass

    def __next_func(self, handler):
        handler(self.req, self.res, self.__next_func)

    def __dispatch(self, req):
        adapter = self.rules.bind_to_environ(req.environ)
        self.req = req
        self.res = SolaceResponse()
        try:
            endpoint, values = adapter.match()
            self.req.params = munch.munchify(values)
            if endpoint not in self.views:
                raise NotFound
            self.views[endpoint](self.req, self.res, self.__next_func)

            if self.res.json:
                self.res.content_type = "application/json"
                self.res.data = json.dumps(self.res.json)
            return self.res
        except HTTPException as e:
            err = {
                'code': e.code,
                'message': e.description
            }
            res = Response(json.dumps({"error": err}), e.code)
            res.content_type = 'application/json'
            return res 

    def __wsgi_app(self, environ, start_response):
        req = Request(environ)
        res = self.__dispatch(req)
        return res(environ, start_response)

    def __call__(self, environ, start_response):
        return self.__wsgi_app(environ, start_response)

class DevelopmentServer:
    
    # TODO: look at more configuration options 
    # that we can support for the DevelopmentServer.
    # https://werkzeug.palletsprojects.com/en/2.0.x/serving/

    def __init__(self, api, host = "127.0.0.1", port = 5000, reload = True):
        self.api = api
        self.host = host
        self.port = port
        self.reload = reload
    
    def start(self):
        run_simple(
            self.host, 
            self.port, 
            self.api, 
            use_debugger=False,
            use_reloader=self.reload
        )
