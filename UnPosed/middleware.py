import re

from django.conf import settings
from unposd.views import login

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
	EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		return response

	def process_view(self, request, view_func, view_args, view_kwargs):
		''' intervene in between each route to see if the user is allowed to view it
			else throw am authentication required alert and route to login page
		'''
		assert hasattr(request, 'user')
		path = request.path_info.lstrip('/')

		if not request.user.is_authenticated:
			if not any(url.match(path) for url in EXEMPT_URLS):
				return login(request, alert="Authentication required!")