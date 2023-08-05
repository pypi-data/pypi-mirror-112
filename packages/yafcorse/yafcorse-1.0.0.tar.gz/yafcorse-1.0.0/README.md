# Yet Another Flask CORS Extension

```bash
pip install yafcorse
```

```python
from flask import Flask

from yafcorse import Yafcorse

def create_app():
    app = Flask(__name__)

    cors = Yafcorse({
        'origins': lambda origin: origin == 'https://api.your-domain.space',
        'allowed_methods': ['GET', 'POST', 'PUT'],
        'allowed_headers': ['Content-Type', 'X-Test-Header'],
        'allow_credentials': True,
        'cache_max_age': str(60 * 5)
    })
    cors.init_app(app)

    return app
```
