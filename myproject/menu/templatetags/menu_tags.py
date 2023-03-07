from django import template
from django.utils.safestring import mark_safe
from ..models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    items = MenuItem.objects.filter(menu__name=menu_name).select_related('menu', 'parent').values(
        'menu__name', 'name', 'parent__name', 'url')
    tree = build_menu_tree(request, items)
    html = render_menu(tree)
    return mark_safe(html)


def get_active_item(request, items):
    """
    Функция возвращает активный элемент меню
    """
    for item in items:
        is_active = request.path == f"/{item['url']}/" if item['url'] else False
        if is_active:
            return item
    return None


def build_menu_tree(request, items, parent=None):
    """
    Функция строит дерево меню
    """
    active_item = get_active_item(request, items)
    tree = []
    for item in items:
        is_active = request.path == f"/{item['url']}/" if item['url'] else False
        if item['parent__name'] == parent:
            node = {
                'name': item['name'],
                'url': item['url'],
                'is_active': is_active,
            }
            # Если текущий элемент активен, показываем его дочерние элементы
            if is_active:
                node['is_open'] = True
                node['children'] = build_menu_tree(request, items, item['name'])
            # Если активен родитель текущего элемента, показываем его дочерние элементы
            elif active_item and active_item['parent__name'] == item['name']:
                node['is_open'] = True
                node['children'] = build_menu_tree(request, items, item['name'])
            # Если текущий элемент имеет дочерние элементы, показываем их
            elif item.get('children'):
                node['children'] = build_menu_tree(request, items, item['name'])
            tree.append(node)
    return tree



def render_menu(menu):
    """
    Функция рендерит меню
    """
    html = "<ul>"
    for item in menu:
        active_class = ' class="active"' if item['is_active'] else ''
        open_class = ' class="open"' if item.get('is_open') else ''
        html += f"<li{open_class}><a href='/{item['url']}/' {active_class}>{item['name']}</a>"
        if item.get("children"):
            html += render_menu(item["children"])
        html += "</li>"
    html += "</ul>"
    return html
