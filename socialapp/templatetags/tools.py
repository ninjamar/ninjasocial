from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from requests.utils import requote_uri
from html import escape
import re

URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

register = template.Library()

@register.filter(name="render_post_content", is_safe=True)
@stringfilter
def render_post_content_filter(text, image):
    urls = re.findall(URL_REGEX, text)
    urls = [escape(i) for i in urls]
    replaced_value = text
    replaced_value = escape(replaced_value)
    for index, url in enumerate(urls):
        replaced_value = replaced_value.replace(url, f"<a href=\"{url}\">{url}</a>", index*2)
    if image == None:
        return mark_safe(f"<p>{replaced_value}</p>")
    else:
        return mark_safe(f"<img src='{escape(requote_uri(image))}'><p>{replaced_value}</p>")

@register.filter(name="have_i_been_reported_by_user", is_safe=True)
def have_been_reported_by_user_filter(post, username):

    reports = post.reports.all()
    if len(reports) > 0:
        for report in reports:
            if username == report.reported_by.username:
                return True
    return False
@register.filter(name="has_user_liked_post", is_safe=True)
def has_user_liked_post_filter(post, username):
    likes = post.likes.all()
    if len(likes) > 0:
        for like in likes:
            if username == like.user.username:
                return True
    return False

@register.filter(name="total_post_likes", is_safe=True)
def total_post_likes_filter(post):
    likes = post.likes.all()
    return len(likes)

@register.filter("profile_about", is_safe=True)
def profile_about_filter(user):
    return mark_safe(escape(user.about))

@register.filter("user_tag", is_safe=True)
def user_tag_filter(user):
    tags = []
    if user.groups.filter(name='Moderator').exists():
        tags.append('<i class="fa-solid fa-diamond"></i>')

    if user.groups.filter(name='Developer').exists():
        tags.append('<i class="fa-brands fa-dev"></i>')

    if user.groups.filter(name='Tester').exists():
        tags.append('<i class="fa-solid fa-vial-circle-check"></i>')

    if user.groups.filter(name='Custom').exists():
        tags.append('<i class="fa-duotone fa-jet-fighter-up"></i>')
    
    return mark_safe(''.join(tags))