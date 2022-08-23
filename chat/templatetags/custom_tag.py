from django import template
import urllib

register = template.Library()

@register.inclusion_tag("chat/translation.html")
def same_name_check(contributor, name, language, chat):
    parse_contributor = urllib.parse.quote(contributor)

    if parse_contributor == name:
        return

    context = {}
    context["language"] = language
    context["chat"] = chat
    return context