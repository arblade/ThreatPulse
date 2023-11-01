import logging
import requests
from base64 import b64encode
from markdownify import MarkdownConverter as OriginalConverter, chomp

from .handlers.base import BaseFeedHandler

logger = logging.getLogger("mdconverter")

class MDConverter(OriginalConverter):
    def __init__(self, handler=BaseFeedHandler, **options):
        super().__init__(**options)
        self.handler = handler
    
    def convert_img(self, el, text, convert_as_inline):
        alt = el.attrs.get('alt', None) or ''
        src = el.attrs.get('src', None) or ''
        title = el.attrs.get('title', None) or ''
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        
        # if there is no source, do not bother
        if src == "":
            return ""
        
        # fetch the image
        logger.debug(f"Downloading img from {src}")
        res = requests.get(el["src"], headers=self.handler.headers)
        img_64 = b64encode(res.content).decode()
            
        if (convert_as_inline
                and el.parent.name not in self.options['keep_inline_images_in']):
            return alt

        return '![%s](%s%s)' % (alt, "data:image/png;base64,"+img_64, title_part)

    def convert_a(self, el, text, convert_as_inline):
        prefix, suffix, text = chomp(text)
        if not text:
            return ''
        href = el.get('href')
        title = el.get('title')
        # For the replacement see #29: text nodes underscores are escaped
        if (self.options['autolinks']
                and text.replace(r'\_', '_') == href
                and not title
                and not self.options['default_title']):
            # Shortcut syntax
            return '<%s>' % href
        if self.options['default_title'] and not title:
            title = href
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        
        # if an anchor
        if href.startswith("#"):
            href = href.replace("_", "-").lower()
        
        return '%s[%s](%s%s)%s' % (prefix, text, href, title_part, suffix) if href else text