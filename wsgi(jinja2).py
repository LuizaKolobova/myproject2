
import os
from wsgiref.simple_server import make_server
from jinja2 import Environment, Template, FileSystemLoader

class Middleware(object):
    def __init__(self, app):
        self.app = app
        
    def __call__(self, environ, start_response):
        for lists in self.app(environ, start_response):
            text = lists
            if text.find('<body') != -1:
                yield text.encode()
                yield "<div class='top'>Middleware TOP</div>".encode()
            elif text.find('</body>') != -1:
                yield "<div class='botton'>Middleware BOTTOM</div>".encode()
                yield text.encode()
            else:
                yield text.encode()


def App(environ,start_response):
    filepath = environ['PATH_INFO']
    environment=Environment(loader=FileSystemLoader('htmlfiles'))
    result=['File not found.']
    template ="";
    if filepath=="/" or filepath=="/index.html":
,        template = environment.get_template('/index.html').render(link1='<h3> <a href="file:///home/lui/Документы/myproject-master/about/aboutme.html">Абсолютная ссылка</a> </h3>',
                                                         link2='<h3> href="/about/aboutme.html">Относительная ссылка</h3>',color='#9411D6'
                                                         text ='<h1><i>Ссылки на  aboutme.html </i> </h1>')
        start_response('200 OK', [('Content-type', 'text/HTML; charset=utf-8')])                                                   
    elif filepath=="/about/aboutme.html":
        template = environment.get_template('/aboutme.html').render((link1='<h3> <a href="file:///home/lui/Документы/myproject-master/index.html">Абсолютная ссылка</a> </h3>',
                                                         link2='<h3> href="/index.html">Абсолютная ссылка</h3>',color='#20B2AA'
                                                         text ='<h1><i>Ссылки на index.html </i> </h1>')
        start_response('200 OK', [('Content-type', 'text/HTML; charset=utf-8')])
    else:
        start_response('404 Not Found', [('Content-Type', 'text/HTML; charset=utf-8')])
        return ''.encode()
    
    return [template]
  
  
  if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = Middleware(App)
    _server = make_server('localhost', 8000, app)
    print ("Serving localhost on port 8000...")
    _server.serve_forever() 
