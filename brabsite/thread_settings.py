# Use this to dynamically change settings variables in middleware instead of direct assignment
# to prevent cross-contamination of threads with wrong values.

# Example:
# from brabs.brabsite.thread_settings import set_thread_vars
## Sets `request.site` and `request.account`
# set_thread_vars(request=request, account=request.account, site=request.site)

# or

# Sets `settings.TEMPLATE_DIRS`
# set_thread_vars(settings=settings, TEMPLATE_DIRS=request.account, site=request.site)
# like below...

# from django.conf import settings
# from brabs.brabsite.thread_settings import set_thread_vars
#
# class MobileTemplatesMiddleware(object):
#     """Determines which set of templates to use for a mobile site"""
#
#     ORIG_TEMPLATE_DIRS = settings.TEMPLATE_DIRS
#
#     def process_request(self, request):
#         # sets are used here, you can use other logic if you have an older version of Python
#         MOBILE_SUBDOMAINS = set(['m', 'mobile'])
#         domain = set(request.META.get('HTTP_HOST', '').split('.'))
#
#         if len(MOBILE_SUBDOMAINS & domain):
#             set_thread_vars(settings=settings, TEMPLATE_DIRS = settings.MOBILE_TEMPLATE_DIRS + self.ORIG_TEMPLATE_DIRS)
#         else:
#             set_thread_vars(settings=settings, TEMPLATE_DIRS = settings.DESKTOP_TEMPLATE_DIRS + self.ORIG_TEMPLATE_DIRS)


from threading import local

from django.conf import *

_thread_locals = local()

def set_thread_vars(**kwargs):
    for key, value in kwargs.items():
        setattr(_thread_locals, key, value)

class ThreadSetting(object):

    def __init__(self, name, value_or_callback=None):
        self.name = name
        self._value_or_callback = value_or_callback
        setattr(_thread_locals, self.name, self)
        setattr(LazySettings, self.name, self)

    def __get__(self, obj, _type=None):
        result = None
        if callable(self._value_or_callback):
            result = self._value_or_callback(**_thread_locals.__dict__)
        else:
            result = self._value_or_callback
        return result

    def __set__(self, obj, value):
        self._value_or_callback = value


# Preserve the original LazySettings get/set
# functions so they can be wrapped later.
old_get_attr = LazySettings.__getattr__
old_set_attr = LazySettings.__setattr__


def my_get_attr(orig_settings, name):
    setting = old_get_attr(orig_settings, name)
    if hasattr(_thread_locals, name):
        setting = getattr(_thread_locals, name)
    return setting


def my_set_attr(orig_settings, name, value):
    if hasattr(_thread_locals, name):
        _thread_locals.__dict__[name].__set__(orig_settings, value)
    else:
        old_set_attr(orig_settings, name, value)

# Alter get/set on the LazySettings object
# to use the thread-aware accessors.
settings.__class__.__getattr__ = my_get_attr
settings.__class__.__setattr__ = my_set_attr
