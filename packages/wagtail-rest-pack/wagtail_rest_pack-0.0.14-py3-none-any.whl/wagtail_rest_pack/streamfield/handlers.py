from django.template.loader import render_to_string

from wagtail.embeds import embeds
from wagtail.embeds.exceptions import EmbedException
from wagtail.core.rich_text import EmbedHandler
from wagtail.embeds import format
from wagtail.embeds.embeds import get_embed
from wagtail.embeds.models import Embed


def embed_to_frontend_html(url):
    try:
        embed = embeds.get_embed(url)
        embed.html = embed.html.replace("feature=oembed", "feature=oembed&autoplay=1")
        add = 'data-thumbnail="%s"' % embed.thumbnail_url
        add += ' data-title="%s"' % embed.title
        embed.html = embed.html.replace(" src=", "%s src=" % add)

        # Render template
        return render_to_string('wagtailembeds/embed_frontend.html', {
            'embed': embed,
        })
    except EmbedException:
        # silently ignore failed embeds, rather than letting them crash the page
        return ''

class ThumbnailedEmbedHandler(EmbedHandler):
    identifier = 'media'

    @staticmethod
    def get_model():
        return Embed

    @staticmethod
    def get_instance(attrs):
        return get_embed(attrs['url'])

    @staticmethod
    def expand_db_attributes(attrs):
        return embed_to_frontend_html(attrs['url'])
