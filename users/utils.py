from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def generate_link(user ,request):
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain    
    protocol = 'http'
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    return f'{protocol}://{domain}/reset/{uid}/{token}'
