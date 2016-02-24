def user_authed_with_uber(view):
    
    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        
