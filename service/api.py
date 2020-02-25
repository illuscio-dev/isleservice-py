from spanserver import SpanAPI

from ._version import __version__
from ._name import SERVICE_NAME


# the service api is declared here
api = SpanAPI(
    title=SERVICE_NAME, version=__version__, openapi="3.0.0", docs_route="/docs"
)
