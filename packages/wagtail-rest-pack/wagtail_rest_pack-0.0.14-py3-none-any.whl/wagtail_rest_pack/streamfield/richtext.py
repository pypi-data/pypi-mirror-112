from rest_framework import serializers
from wagtail.core.blocks import RichTextBlock

from wagtail.core.templatetags.wagtailcore_tags import richtext as richtext_filter


def rich_text():
    return RichTextSerializer.block_definition()


class RichTextSerializer(serializers.Serializer):
    block_name = 'richtext'
    text = serializers.SerializerMethodField('get_text')

    @staticmethod
    def block_definition():
        features = ['h2', 'h3', 'italic', 'bold', 'ol', 'ul', 'hr', 'link',
                    'document-link', 'image', 'embed', 'code',
                    'superscript', 'subscript', 'strikethrough', 'blockquote']
        return RichTextSerializer.block_name, RichTextBlock(features=features,icon='doc-full')

    class Meta:
        fields = ('text',)

    def get_text(self, value):
        return richtext_filter(value.source)
