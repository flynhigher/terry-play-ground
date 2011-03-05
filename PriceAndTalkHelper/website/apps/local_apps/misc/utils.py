
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import re
import unicodedata
from htmlentitydefs import name2codepoint
from django.utils.encoding import smart_unicode, force_unicode

_inbox_count_sources = None

def inbox_count_sources():
    global _inbox_count_sources
    if _inbox_count_sources is None:
        sources = []
        for path in settings.COMBINED_INBOX_COUNT_SOURCES:
            i = path.rfind('.')
            module, attr = path[:i], path[i+1:]
            try:
                mod = __import__(module, {}, {}, [attr])
            except ImportError, e:
                raise ImproperlyConfigured('Error importing request processor module %s: "%s"' % (module, e))
            try:
                func = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a "%s" callable request processor' % (module, attr))
            sources.append(func)
        _inbox_count_sources = tuple(sources)
    return _inbox_count_sources


def get_send_mail():
    """
    A function to return a send_mail function suitable for use in the app. It
    deals with incompatibilities between signatures.
    """
    # favour django-mailer but fall back to django.core.mail
    if "mailer" in settings.INSTALLED_APPS:
        from mailer import send_mail
    else:
        from django.core.mail import send_mail as _send_mail
        def send_mail(*args, **kwargs):
            del kwargs["priority"]
            return _send_mail(*args, **kwargs)
    return send_mail

def slugify(s, entities=True, decimal=True, hexadecimal=True, model=None, slug_field='slug', pk=None):
    s = smart_unicode(s)
    # we don't want a string > 40 characters
    if len(s) > 40:
        s = s[:40]

    #character entity reference
    if entities:
        s = re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), s)

    #decimal character reference
    if decimal:
        try:
            s = re.sub('&#(\d+);', lambda m: unichr(int(m.group(1))), s)
        except:
            pass

    #hexadecimal character reference
    if hexadecimal:
        try:
            s = re.sub('&#x([\da-fA-F]+);', lambda m: unichr(int(m.group(1), 16)), s)
        except:
            pass

    #translate
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')

    #replace unwanted characters
    s = re.sub(r'[^-a-z0-9]+', '-', s.lower())

    #remove redundant -
    s = re.sub('-{2,}', '-', s).strip('-')

    slug = s
    if model:  
        # return unique slug for a model (appending integer counter)
        def get_query():
            query = model.objects.filter(**{ slug_field: slug })
            if pk:
                query = query.exclude(pk=pk)
            return query
        counter = 2
        while get_query():
            slug = "%s-%s" % (s, counter)
            counter += 1
    return slug
