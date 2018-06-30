import re

from django.core.exceptions import ValidationError
from django.db.models import CharField

from django_tagify.widgets import TagsInput


class TagsField(CharField):
    description = 'Tags'

    def __init__(self, widget_settings=None, *args, **kwargs):
        # Widget settings
        self.widget_settings = {
            'delimiter': ','
        }

        if widget_settings is not None:
            self.widget_settings.update(widget_settings)

        # Defaults
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

        while len(value) >= 2 and value[-2:-1] != '\\' and value[-1:] == '"':
            value = value[:-1]

        delimiter = self.widget_settings['delimiter']
        value = value.replace('"%s"' % delimiter, delimiter)
        return value

    def validate(self, value, model_instance):
        tags = value.split(self.widget_settings['delimiter'])
        no_tags = len(tags) == 1 and tags[0] == ''

        # widget_settings validation
        if 'maxTags' in self.widget_settings:
            if len(tags) > self.widget_settings['maxTags']:
                raise ValidationError('The number of tags specified is greater than maxTags.')

        if 'pattern' in self.widget_settings:
            for tag in tags:
                if not re.match(self.widget_settings['pattern'], tag):
                    raise ValidationError('Tag did not match pattern.')

        if not no_tags:
            if 'duplicates' in self.widget_settings and self.widget_settings['duplicates'] is False:
                for tag in tags:
                    if tags.count(tag) > 1:
                        raise ValidationError('Duplicate tags are not allowed.')

            if 'enforceWhitelist' in self.widget_settings and self.widget_settings['enforceWhitelist'] is True:
                for tag in tags:
                    if tag not in self.widget_settings['whitelist']:
                        raise ValidationError('Tag is not in whitelist.')

            if 'blacklist' in self.widget_settings:
                for tag in tags:
                    if tag in self.widget_settings['blacklist']:
                        raise ValidationError('Tag is in blacklist.')

        # Regular CharField validation
        super(TagsField, self).validate(value, model_instance)

    def formfield(self, **kwargs):
        kwargs['widget'] = TagsInput({'class': 'form-control'}, self.widget_settings)
        return super(TagsField, self).formfield(**kwargs)
