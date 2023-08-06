from rest_framework import serializers
from wagtail.core import blocks
from wagtail.core.blocks import RichTextBlock, StructBlock, PageChooserBlock
from wagtail.core.models import Page

from wagtail.core.templatetags.wagtailcore_tags import richtext as richtext_filter
from wagtail.snippets.blocks import SnippetChooserBlock
from django.utils.translation import gettext_lazy as _

from wagtail_rest_pack.streamfield.serializers import SettingsStreamFieldSerializer


def page_list():
    return PageListSerializer.block_definition()


page_list_variants = [
    ('simple', _('Simple')),
    ('amazing', _('Top, Top Three and simple')),
    ('nested', _('Directly draw all pages inside')),
]


class PageListSerializer(serializers.Serializer):
    block_name = 'pagelist'
    variant = serializers.ChoiceField(page_list_variants)
    children_of = serializers.SerializerMethodField('get_page_id')

    @staticmethod
    def block_definition():
        return PageListSerializer.block_name, PageListStruct(label=_('List children of selected page'))

    class Meta:
        fields = ('variant', 'children_of',)

    def get_page_id(self, value):
        return value['children_of'].id

class PageListStruct(blocks.StructBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(local_blocks=[
            ('children_of', PageChooserBlock(label=_('List children of selected page'))),
            ('variant',
             blocks.ChoiceBlock(choices=page_list_variants, label=_('A variant how children should be displayed.')))
        ], icon='folder-open-1', **kwargs)
