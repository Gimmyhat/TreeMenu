from django import template
from django.utils.safestring import mark_safe

from ..models import Menu

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    try:
        current_path = context['request'].path_info.lstrip('/')
        context['current_path'] = current_path
    except KeyError:
        return ''
    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return ''
    menu_items = menu.menuitem_set.all()
    menu_tree = build_menu_tree(menu_items)
    menu_html = render_menu_tree(menu_tree, current_path)
    return mark_safe(menu_html)


def build_menu_tree(menu_items):
    menu_items_dict = {menu_item.id: menu_item for menu_item in menu_items}
    menu_tree = []
    for menu_item in menu_items:
        if not menu_item.parent_id:
            menu_tree.append(menu_item)
        else:
            parent = menu_items_dict.get(menu_item.parent_id)
            if parent:
                if not hasattr(parent, 'children'):
                    setattr(parent, 'children', [])
                parent.children.add(menu_item)
    return menu_tree


def render_menu_tree(menu_tree, current_path):
    menu_html = '<ul>'
    for menu_item in menu_tree:
        menu_item_url = menu_item.url or '#'
        is_active = current_path.startswith(menu_item_url)
        children = getattr(menu_item, 'children', [])
        is_expanded = is_active or any(child for child in children.all() if current_path.startswith(child.url or ''))
        menu_html += f'<li class="{"active" if is_active else ""} {"expanded" if is_expanded else ""}">'
        menu_html += f'<a href="{menu_item_url if menu_item_url != "#" else ""}{menu_item.url_name if not menu_item_url else ""}">'
        menu_html += menu_item.name
        menu_html += '</a>'
        if children:
            menu_html += render_menu_tree(children.all(), current_path)
        menu_html += '</li>'
    menu_html += '</ul>'
    return menu_html
