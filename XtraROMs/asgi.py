import os
from django.core.asgi import get_asgi_application
from hypercorn.config import Config
from hypercorn.asyncio import serve

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'XtraROMs.settings')

application = get_asgi_application()

# This is the entry point that Hypercorn will use
def run_hypercorn():
    config = Config()
    config.bind = [f'{os.environ.get("HOST", "0.0.0.0")}:{os.environ.get("PORT", "8000")}']
    serve(application, config)

# Start the Hypercorn server
if __name__ == "__main__":
    run_hypercorn()
