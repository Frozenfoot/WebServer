from pprint import pformat
from cgi import parse_qsl, escape

def application(environ, start_response):
    output = "Gunicorn Hello world\n<p>WSGI!</p>"

    output += 'Post:'
    output += '<form method="post">'
    output += '<input type="text" name = "test">'
    output += '<input type="submit" value="Send">'
    output += '</form>'

    d = parse_qsl(environ['QUERY_STRING'])
    if environ['REQUEST_METHOD'] == 'POST':
        output += '<h1>Post  data:</h1>'
        output += pformat(environ['wsgi.input'].read())

    if environ['REQUEST_METHOD'] == 'GET':
        if environ['QUERY_STRING'] != '':
            output += '<h1>Get data:</h1>'
            for ch in d:
                output += ' = '.join(ch)
                output += '<br>'

    output_len = sum(len(line) for line in output)
    start_response('200 OK', [('Content-type', 'text/html'),
                              ('Content-Length', str(output_len))])
    return [bytes(output, encoding = 'utf-8')]