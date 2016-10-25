from django.http import HttpResponse
from pprint import pformat
from cgi import parse_qsl, escape

def getAndPostRequests(request):
    output = 'This is page is given by Django\n'
    print ('Request is: ', request.method)
    output += '<br>'
    output += str('Request method is: ' + request.method  + '<br>')
    output += str('GET requests:' + '<br>')
    getItems = request.GET.items()

    for item in getItems:
        print (item)
        output += str(item)
        output += '<br>'

    getItems = request.POST.items()

    for item in getItems:
        print(item)
        output += str(item)
        output += '<br>'

    return HttpResponse(output)
