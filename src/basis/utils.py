from basis.cache import expire_cache
from basis.models import ProxyServer


@expire_cache()
def get_active_proxy():
    return ProxyServer.get_active()
