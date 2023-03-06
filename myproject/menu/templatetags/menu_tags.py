from django import template
from django.utils.safestring import mark_safe

from ..models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    try:
        current_path = context['request'].path_info.lstrip('/')
        context['path'] = current_path
    except KeyError:
        return ''
    result = MenuItem.objects.filter(menu__name=menu_name).select_related('menu', 'parent').values(
        'menu__name', 'name', 'parent__name', 'url')
    tree = build_menu_tree(result)
    html = render_menu(tree)
    return mark_safe(html)


def build_menu_tree(items, parent=None):
    tree = []
    for item in items:
        if item['parent__name'] == parent:
            node = {
                'name': item['name'],
                'url': item['url'],
                'children': build_menu_tree(items, item['name'])
            }
            tree.append(node)
    return tree


def render_menu(menu):
    html = "<ul>"
    for item in menu:
        html += f"<li><a href='{item['url']}'>{item['name']}</a>"
        if item["children"]:
            html += render_menu(item["children"])
        html += "</li>"
    html += "</ul>"
    return html
