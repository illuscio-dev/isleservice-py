import pathlib
import importlib
import sys
from .api import api
from ._name import SERVICE_NAME

# Here we import all routes in the routes folder. That way we can just make new routes
# as desired without having to worry about adding them to an import list.
sys.stderr.write(f"STARTING UP: {SERVICE_NAME}\n")

route_files = (pathlib.Path(__file__).parent / "routes").rglob("*.py")

sys.stderr.write(f"CURRENT PATH: {pathlib.Path(__file__).parent}\n")
route_modules = [
    f.stem for f in route_files if f.is_file() and not str(f).startswith("_")
]

for this_route in route_modules:
    sys.stderr.write(f"ROUTE MODULE FOUND: {this_route}\n")
    importlib.import_module(f"service.routes.{this_route}", "service")


# Then declare the function that starts the service.
def start() -> None:
    for route_name in api.router.routes:
        sys.stderr.write(f"ROUTE FOUND: {route_name}\n")
    api.run(address="0.0.0.0", port=80)
