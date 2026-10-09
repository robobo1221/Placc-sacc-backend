import hmac
import ipaddress
import logging

from django.conf import settings
from django.http import HttpResponseNotFound

logger = logging.getLogger(__name__)


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


class APIKeyMiddleware(AdminIPRestrictionMiddleware):
    """Require a shared secret on /api/ (header X-Api-Key) - meant for the server-side frontend (Cloudflare Worker).

    - API_SHARED_SECRET empty: middleware does nothing.
    - API_KEY_ENFORCE False: requests without a valid key are allowed but logged (rollout / verification).
    - API_KEY_ENFORCE True: requests without a valid key get a plain 404.
    Requests from API_KEY_EXEMPT_NETWORKS (home LAN / Tailscale) never need the key.
    Client IP detection (TRUSTED_PROXIES / X-Forwarded-For) is shared with AdminIPRestrictionMiddleware.
    """

    def __init__(self, get_response):
        super().__init__(get_response)
        self.secret = (settings.API_SHARED_SECRET or '').encode()
        self.enforce = settings.API_KEY_ENFORCE
        self.exempt = _networks(settings.API_KEY_EXEMPT_NETWORKS)

    def __call__(self, request):
        if self.secret and request.path.startswith('/api/'):
            ip = self.client_ip(request)
            if not self._in(ip, self.exempt):
                given = request.META.get('HTTP_X_API_KEY', '').encode()
                if not hmac.compare_digest(given, self.secret):
                    if self.enforce:
                        return HttpResponseNotFound()
                    logger.warning('API request without valid X-Api-Key from %s (%s) - not enforced', ip, request.path)
        return self.get_response(request)
