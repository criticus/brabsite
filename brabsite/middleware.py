from django.conf import settings
from brabsite.thread_settings import set_thread_vars

class MobileTemplatesMiddleware(object):
    """Determines which set of templates to use for a mobile site"""

    ORIG_TEMPLATE_DIRS = settings.TEMPLATE_DIRS

    def process_request(self, request):
        # sets are used here, you can use other logic if you have an older version of Python
        MOBILE_SUBDOMAINS = set(['m', 'mobile'])
        domain = set(request.META.get('HTTP_HOST', '').split('.'))

        if len(MOBILE_SUBDOMAINS & domain):
            set_thread_vars(settings=settings, TEMPLATE_DIRS=settings.MOBILE_TEMPLATE_DIRS + self.ORIG_TEMPLATE_DIRS)
        else:
            set_thread_vars(settings=settings, TEMPLATE_DIRS=settings.DESKTOP_TEMPLATE_DIRS + self.ORIG_TEMPLATE_DIRS)
