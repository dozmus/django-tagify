from django.forms.renderers import DjangoTemplates
from django.test import SimpleTestCase

from django_tagify.fields import TagsField
from django_tagify.widgets import TagsInput


# class WidgetTest(SimpleTestCase):
#     beatles = (('J', 'John'), ('P', 'Paul'), ('G', 'George'), ('R', 'Ringo'))
#
#     @classmethod
#     def setUpClass(cls):
#         cls.django_renderer = DjangoTemplates()
#         cls.renderers = [cls.django_renderer]
#         super().setUpClass()
#
#     def check_html(self, widget, name, value, html='', attrs=None, strict=False, **kwargs):
#         assert_equal = self.assertEqual if strict else self.assertHTMLEqual
#         output = widget.render(name, value, attrs=attrs, renderer=self.django_renderer, **kwargs)
#         assert_equal(output, html)
#
#
# class TagsInputTest(WidgetTest):
#     widget = TagsInput()
#
#     def test_render(self):
#         self.check_html(self.widget, 'tags', '', html='')


class TagsFieldTest(SimpleTestCase):
    def test_to_python_vbar_delimeter(self):
        self.test_to_python(delimiter='|')

    def test_to_python(self, delimiter=','):
        field = TagsField(widget_settings={'delimiter': delimiter})
        self.assertEquals(field.to_python('tag'), 'tag')
        self.assertEquals(field.to_python(''), '')
        self.assertEquals(field.to_python('tag1%stag2' % delimiter), 'tag1%stag2' % delimiter)
        self.assertEquals(field.to_python('"tag1"%s"tag2"' % delimiter), 'tag1%stag2' % delimiter)
        self.assertEquals(field.to_python('"tag1"%s"tag2\\""' % delimiter), 'tag1%stag2\\"' % delimiter)
