from django.conf import settings
from brabsite.thread_settings import set_thread_vars
import os.path

def load_from_agents_file():
    f = None
    try:
        if settings.MOBILE_USER_AGENTS_FILE:
            f = open(settings.MOBILE_USER_AGENTS_FILE)
        else:
            f = open((
                os.path.join(os.path.abspath(os.path.dirname(__file__)).replace('\\','/'), 'mobile_agents.txt').replace('\\','/'),
            ))
        ss = f.readlines()
    finally:
        if f:
            f.close()
    return [s.strip() for s in ss if not s.startswith('#') and s not in settings.MOBILE_IGNORE_LIST]


class MobileTemplatesMiddleware(object):
    """Determines which set of templates to use for a mobile site"""

    ORIG_TEMPLATE_DIRS = settings.TEMPLATE_DIRS
    USER_AGENTS = load_from_agents_file()

    def process_request(self, request):

        is_mobile = False

        if 'opera mini' not in settings.MOBILE_IGNORE_LIST and request.META.has_key("HTTP_X_OPERAMINI_FEATURES"):
            #opera mini.
            # http://dev.opera.com/articles/view/opera-mini-request-headers/
            #this is a mobile request
            is_mobile=True

        elif request.META.has_key('HTTP_USER_AGENT'):
            user_agent = request.META['HTTP_USER_AGENT']

            for ua in self.USER_AGENTS:
                if ua in user_agent:
                    is_mobile=True
                    break

        if 'wap' not in settings.MOBILE_IGNORE_LIST and request.META.has_key("HTTP_ACCEPT"):
            s = request.META["HTTP_ACCEPT"].lower()
            if 'application/vnd.wap.xhtml+xml' in s:
                # Then it's a wap browser
                is_mobile=True

        if is_mobile:
            set_thread_vars(settings=settings, TEMPLATE_DIRS=settings.MOBILE_TEMPLATE_DIRS)
            set_thread_vars(request=request, mobile=True)
        else:
            set_thread_vars(settings=settings, TEMPLATE_DIRS=settings.DESKTOP_TEMPLATE_DIRS)
            set_thread_vars(request=request, mobile=False)
