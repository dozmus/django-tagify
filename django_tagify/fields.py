from django.db.models import CharField

from django_tagify.widgets import TagsInput


class TagsField(CharField):
    description = 'Tags'

    def __init__(self, widget_settings=None, *args, **kwargs):
        self.widget_settings = widget_settings or {}
        defaults = {
            'help_text': 'Press enter or comma after each tag you define.',
        }
        defaults.update(kwargs)
        super(TagsField, self).__init__(*args, **defaults)

    def to_python(self, value):
        if value is None or value == '':
            return value

        # value from the TagsInput are en-quoted and comma-separated
        value = value.lstrip('"')
        value = value.rstrip('"')
        value = value.replace('","', ',')
        return value

    def formfield(self, **kwargs):
        kwargs['widget'] = TagsInput({'class': 'form-control'}, self.widget_settings)
        return super(TagsField, self).formfield(**kwargs)
