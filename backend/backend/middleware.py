import ipaddress

from django.conf import settings
from django.http import HttpResponseNotFound


def _networks(values):
    return [ipaddress.ip_network(v.strip(), strict=False) for v in values if v and v.strip()]


class AdminIPRestrictionMiddleware:
    """Only allow /admin from ADMIN_ALLOWED_NETWORKS; everyone else gets a plain 404.

    Behind a reverse proxy the real client is taken from X-Forwarded-For, but only when the
    request comes from a TRUSTED_PROXIES address (otherwise the header could be forged).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed = _networks(settings.ADMIN_ALLOWED_NETWORKS)
        self.proxies = _networks(settings.TRUSTED_PROXIES)

    def _in(self, ip, networks):
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return False
        return any(addr in net for net in networks)

    def client_ip(self, request):
        ip = request.META.get('REMOTE_ADDR', '')
        if self.proxies and self._in(ip, self.proxies):
            # Walk X-Forwarded-For from the right (closest hop) and skip our own proxies.
            for hop in reversed(request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')):
                hop = hop.strip()
                if hop and not self._in(hop, self.proxies):
                    return hop
        return ip

    def __call__(self, request):
        if request.path.startswith('/admin') and not self._in(self.client_ip(request), self.allowed):
            return HttpResponseNotFound()
        return self.get_response(request)
