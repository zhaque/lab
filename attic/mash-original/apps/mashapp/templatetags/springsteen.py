from django import template
register = template.Library()


def clean_url(word, length=75):
    """Return a URL for display only, without protocol://, and up to length characters.
    
    We add ... if the URL is truncated.
    
    """
    parts = word.split('//')
    if len(parts) > 1:
        word = parts[1]
    if len(word) > length:
        return "%s ..." % word[:length-4]
    return word

register.filter('clean_url', clean_url)
