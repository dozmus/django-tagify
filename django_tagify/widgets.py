from django.forms import Textarea


class TagsInput(Textarea):
    template_name = 'tagsinput.html'

    def __init__(self, attrs=None, tagify_settings=None):
        """
        :param tagify_settings: Various settings used to configure Tagify.
        You can specify if 'duplicates' are allowed (boolean).
        You can specify 'autocomplete' (boolean) - this matches from the whitelist.
        You can specify 'enforceWhitelist' (boolean).
        You can specify 'maxTags' (int).
        You can specify the 'whitelist' (string list).
        You can specify the 'blacklist' (string list).
        You can specify the 'delimiter' (string).
        You can specify the RegEx 'pattern' to validate the input (string).
        """
        # TODO validate settings
        super().__init__(attrs)
        self.tagify_settings = tagify_settings or {}

    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)

        if 'tagify_settings' not in ctx:
            ctx['tagify_settings'] = self.tagify_settings
        return ctx

    class Media:
        js = ('js/tagify.js', 'js/tagify.polyfills.js', 'js/jQuery.tagify.min.js')
        css = {'all': ('css/tagify.css', )}
