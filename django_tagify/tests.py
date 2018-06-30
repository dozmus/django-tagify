from django.core.exceptions import ValidationError
from django.forms.renderers import DjangoTemplates
from django.test import SimpleTestCase

from django_tagify.fields import TagsField
from django_tagify.widgets import TagsInput


class WidgetTest(SimpleTestCase):
    beatles = (('J', 'John'), ('P', 'Paul'), ('G', 'George'), ('R', 'Ringo'))

    @classmethod
    def setUpClass(cls):
        cls.django_renderer = DjangoTemplates()
        cls.renderers = [cls.django_renderer]
        super().setUpClass()

    def check_html(self, widget, name, value, html='', attrs=None, strict=False, **kwargs):
        assert_equal = self.assertEqual if strict else self.assertHTMLEqual
        output = widget.render(name, value, attrs=attrs, renderer=self.django_renderer, **kwargs)
        assert_equal(output, html)


class TagsInputTest(WidgetTest):
    def test_render(self):
        widget = TagsInput()
        self.check_html(widget, 'tags', '', html="""<textarea name="tags" cols="40" rows="10"></textarea>
        <script type="text/javascript">
            var input = document.querySelector('textarea[name=tags]'), tagify = new Tagify(input, { });
        </script>""")

    def test_render_with_value(self):
        widget = TagsInput()
        self.check_html(widget, 'tags', 'tag1,tag2',
                        html="""<textarea name="tags" cols="40" rows="10">tag1,tag2</textarea>
        <script type="text/javascript">
            var input = document.querySelector('textarea[name=tags]'), tagify = new Tagify(input, { });
        </script>""")

    def test_render_with_settings(self):
        tagify_settings = {
            'duplicates': True,
            'autocomplete': False,
            'enforceWhitelist': False,
            'maxTags': 10,
            'whitelist': ['word1', 'word2'],
            'blacklist': [],
            'delimeter': ',',
            'pattern': '^[A-Za-z]+$',
        }
        widget = TagsInput(tagify_settings=tagify_settings)

        # Assert
        self.check_html(widget, 't', '', html="""<textarea name="t" cols="40" rows="10"></textarea>
        <script type="text/javascript">
            var input = document.querySelector('textarea[name=t]'), tagify = new Tagify(input, {
                'duplicates': true,
                'autocomplete': false,
                'enforceWhitelist': false,
                'maxTags': 10,
                'whitelist': ['word1', 'word2'],
                'blacklist': [],
                'delimeter': ',',
                'pattern': '^[A-Za-z]+$',
            });
        </script>""")


class TagsFieldTest(SimpleTestCase):
    def test_validation_duplicates(self):
        field = TagsField(widget_settings={'duplicates': False})
        self.assertRaises(ValidationError, lambda: field.validate('tag,tag', None))
        field.validate('tag,tag ', None)  # expected: no exception

    def test_validation_whitelist(self):
        field = TagsField(widget_settings={'enforceWhitelist': True, 'whitelist': ['a', 'b', 'c']})
        self.assertRaises(ValidationError, lambda: field.validate('a,b,c,d', None))
        field.validate('a', None)  # expected: no exception
        field.validate('a,b,c', None)  # expected: no exception

    def test_validation_whitelist_blank_input(self):
        field = TagsField(widget_settings={'enforceWhitelist': True, 'whitelist': ['a', 'b', 'c']}, blank=True)
        field.validate('', None)  # expected: no exception

    def test_validation_maxTags(self):
        field = TagsField(widget_settings={'maxTags': 5})
        self.assertRaises(ValidationError, lambda: field.validate('a,b,c,d,e,f', None))
        field.validate('a,b,c,d,e', None)  # expected: no exception

    def test_validation_blacklist(self):
        field = TagsField(widget_settings={'blacklist': ['bad word', 'bad!']})
        self.assertRaises(ValidationError, lambda: field.validate('bad word', None))
        self.assertRaises(ValidationError, lambda: field.validate('bad!', None))
        self.assertRaises(ValidationError, lambda: field.validate('this is ok,bad!', None))
        field.validate('this is ok,not bad!', None)  # expected: no exception

    def test_validation_blacklist_blank_input(self):
        field = TagsField(widget_settings={'blacklist': ['bad word', 'bad!']}, blank=True)
        field.validate('', None)  # expected: no exception

    def test_validation_pattern(self):
        field = TagsField(widget_settings={'pattern': '^[a-z][A-Za-z]*$'})
        self.assertRaises(ValidationError, lambda: field.validate('Hello', None))
        field.validate('valid', None)  # expected: no exception

    def test_to_python_vbar_delimeter(self):
        self.test_to_python(delimiter='|')

    def test_to_python(self, delimiter=','):
        field = TagsField(widget_settings={'delimiter': delimiter})
        self.assertEquals(field.to_python('tag'), 'tag')
        self.assertEquals(field.to_python(''), '')
        self.assertEquals(field.to_python('tag1%stag2' % delimiter), 'tag1%stag2' % delimiter)
        self.assertEquals(field.to_python('"tag1"%s"tag2"' % delimiter), 'tag1%stag2' % delimiter)
        self.assertEquals(field.to_python('"tag1"%s"tag2\\""' % delimiter), 'tag1%stag2\\"' % delimiter)
