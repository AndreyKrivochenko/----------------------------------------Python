def secret_front(request):
    request['secret'] = 'some secret'

    
def other_front(request):
    request['key'] = 'value'
