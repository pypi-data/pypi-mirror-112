# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bareasgi_prometheus', 'bareasgi_prometheus.metrics']

package_data = \
{'': ['*']}

install_requires = \
['bareASGI>=3,<4', 'jetblack-metrics>=1,<2', 'prometheus_client>=0.11,<0.12']

setup_kwargs = {
    'name': 'bareasgi-prometheus',
    'version': '3.7.0',
    'description': 'Prometheus metrics for bareASGI',
    'long_description': "# bareASGI-prometheus\n\n[Prometheus](https://prometheus.io/) metrics for bareASGI (read the [docs](https://rob-blackbourn.github.io/bareASGI-prometheus/)).\n\n## Installation\n\nInstall from the pie store\n\n```bash\n$ pip install bareASGI-prometheus\n```\n\n## Usage\n\nThe middleware can either be configured manually or with a helper.\n\n### Manual Configuration\n\n```python\nfrom bareasgi import Application\nfrom bareasgi_prometheus import PrometheusMiddleware, prometheus_view\n\n...\n\nprometheus_middleware = PrometheusMiddleware()\napp = Application(middlewares=[prometheus_middleware])\napp.http_router.add({'GET'}, '/metrics', prometheus_view)\n```\n\n\n### Helper Configuration\n\n```python\nfrom bareasgi import Application\nfrom bareasgi_prometheus import add_prometheus_middleware\n\n...\n\napp = Application()\nadd_prometheus_middleware(app)\n```\n",
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rob-blackbourn/bareASGI-prometheus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
