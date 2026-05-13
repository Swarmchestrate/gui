from django.conf import settings

if settings.DEBUG is True:
    from .mock_config import (
        MockApiClient as BaseApiClient,
        MockEndpoint as BaseEndpoint,
    )
else:
    from .live_config import (
        LiveApiClient as BaseApiClient,
        LiveEndpoint as BaseEndpoint,
    )