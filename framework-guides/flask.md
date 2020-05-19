---
Title: Flask
...

# Flask

Here's a sample Flask server[^1]:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

**Make sure to save your code as `public/app.py`.** If you have any other custom modules that your code imports, put them in `public` too.

First, select a Python Docker image for your site (see [Custom Docker Images](/quick-start/site-configuration.md#custom-docker-images)). Then, in the terminal, create a virtual environment with `virtualenv public/venv`. Activate the virtual environment with `source public/venv/bin/activate`, then install any Python packages you need (like Flask itself) with `pip install <package names>`. If you later need to modify something in your virtual environment, you can always re-activate it with `source public/venv/bin/activate`.

As long as you save your code in the `public` directory, the default `run.sh` template should "just work" (but make sure the command labeled "Flask" is uncommented).

[^1]: <small>Taken from [the Flask Quickstart](https://flask.palletsprojects.com/en/1.1.x/quickstart/)</small>
