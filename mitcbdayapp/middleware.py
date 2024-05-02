import django_browser_reload.middleware


class BrowserReloadMiddleware(django_browser_reload.middleware.BrowserReloadMiddleware):

    def __call__(self, request):
        # Reloading should only be enabled for GET requests
        if request.method == "POST":
            return self.get_response(request)
        else:
            return super().__call__(request)
