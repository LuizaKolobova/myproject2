from wsgiref.simple_server import make_server
from jinja2 import Environment,  FileSystemLoader

class Middleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        for array in self.app(environ, start_response):
            str = array.split("\n")
            for strs in str:
                if strs.find('<body') != -1:
                    yield strs.encode()
                    yield "<div class='top'>Middleware TOP</div>".encode()
                else:
                    if strs.find("</body") != -1:
                        yield "<div class='botton'>Middleware BOTTOM</div>".encode()
                        yield strs.encode()
                    else:
                        yield strs.encode()


def App(environ,start_response):
    filepath = environ['PATH_INFO']
    environment=Environment(loader=FileSystemLoader('htmlfiles'))
    template ="";
    if filepath=="/" or filepath=="/index.html":
        template = environment.get_template('/index.html').render(link1='<h3> <a href="http://localhost:8000/about/aboutme.html">Абсолютная ссылка</a> </h3>',
                                                         link2='<h3> <a href="/about/aboutme.html">Относительная ссылка </a></h3>',color='{color: #FF1493;}',
                                                         text ='<h1><i>Ссылки на  aboutme.html </i> </h1>')
        start_response('200 OK', [('Content-type', 'text/HTML; charset=utf-8')])
    elif filepath=="/about/aboutme.html":
        template = environment.get_template('/aboutme.html').render(link1='<h3> <a href="http://localhost:8000/index.html">Абсолютная ссылка</a> </h3>',
                                                         link2='<h3><a href="/index.html">Относительная ссылка </a></h3>',color='{color: #FFFF00;}',
                                                         text ='<h1><i>Ссылки на index.html </i> </h1>')
        start_response('200 OK', [('Content-type', 'text/HTML; charset=utf-8')])
    else:
        start_response('404 Not Found', [('Content-Type', 'text/HTML; charset=utf-8')])
        return ''.encode()
    
    return [template]
  
if __name__ == '__main__':
    app = Middleware(App)
    _server = make_server('localhost', 8000, app)
    print ("Serving localhost on port 8000...")
    _server.serve_forever() 
