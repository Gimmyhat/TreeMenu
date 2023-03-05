from django.test import TestCase
from django.urls import reverse

from .models import MenuItem
from .templatetags.menu_tags import draw_menu


class MenuTests(TestCase):
    def setUp(self):
        self.menu_item_1 = MenuItem.objects.create(
            name='Home',
            url='/'
        )
        self.menu_item_2 = MenuItem.objects.create(
            name='About',
            url='/about/'
        )
        self.menu_item_3 = MenuItem.objects.create(
            name='Contact',
            url='/contact/'
        )
        self.menu_item_4 = MenuItem.objects.create(
            name='Blog',
            url='/blog/'
        )
        self.menu_item_5 = MenuItem.objects.create(
            name='Portfolio',
            url='/portfolio/'
        )
        self.menu_item_6 = MenuItem.objects.create(
            name='Resume',
            url='/resume/'
        )

        self.menu_item_2.parent = self.menu_item_1
        self.menu_item_2.save()

        self.menu_item_3.parent = self.menu_item_1
        self.menu_item_3.save()

        self.menu_item_4.parent = self.menu_item_1
        self.menu_item_4.save()

        self.menu_item_5.parent = self.menu_item_4
        self.menu_item_5.save()

        self.menu_item_6.parent = self.menu_item_4
        self.menu_item_6.save()

    def test_menu_item_str(self):
        self.assertEqual(str(self.menu_item_1), 'Home')

    def test_menu_item_get_absolute_url(self):
        url = reverse('menu:menu_item', args=[self.menu_item_1.pk])
        self.assertEqual(self.menu_item_1.get_absolute_url(), url)

    def test_draw_menu(self):
        expected_html = (
            '<ul>\n'
            '  <li class="active"><a href="/">Home</a>\n'
            '    <ul>\n'
            '      <li><a href="/about/">About</a></li>\n'
            '      <li><a href="/contact/">Contact</a></li>\n'
            '      <li><a href="/blog/">Blog</a>\n'
            '        <ul>\n'
            '          <li><a href="/portfolio/">Portfolio</a></li>\n'
            '          <li><a href="/resume/">Resume</a></li>\n'
            '        </ul>\n'
            '      </li>\n'
            '    </ul>\n'
            '  </li>\n'
            '</ul>'
        )
        rendered_html = draw_menu('main_menu')
        self.assertHTMLEqual(rendered_html, expected_html)
