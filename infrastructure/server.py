from .app import create_app
from .config import get_config
from .providers.container import create_container

config = get_config()
container = create_container()
app = create_app(container, config)
