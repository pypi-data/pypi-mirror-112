# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linkurious']

package_data = \
{'': ['*']}

install_requires = \
['tortilla>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'linkurious',
    'version': '0.1.0',
    'description': 'Python wrapper around linkurious API',
    'long_description': '## Description\n\nlinkurious is a [tortilla](https://github.com/tortilla/tortilla) based python wrapper around the\n[Linkurious HTTP REST API](https://doc.linkurio.us/server-sdk/latest/apidoc/)\nthat allows users to remotely manage a Linkurious instance, performing the same tasks\nthat can be done through the web application.\n\nThis can be useful to:\n- automate some of the most tedious tasks\n- integrate the Linkurious instance within a wider multi-services application\n\n[Linkurious Enterprise](https://linkurio.us/product/) is a copyrighted graph visualization and analysis platform,\nthat allows users to perform queries and build visualizations on multiple graph databases (Neo4j, CosmosDB, JanusGraph).\n\n## Installation\n\nPython versions from 3.6 are supported.\n\nThe package is hosted on pypi, and can be installed, for example using pip:\n\n    pip install linkurious\n\n## Usage\nThe package only has one class (and one exception), creating a `Linkurious` instance passing username and password\nwill connect to the instance. All following operations will be performed using the same user session. \n\n    from linkurious import Linkurious\n    \n    # login\n    l = Linkurious(\n        host=\'https://linkurious.example.org\', \n        username=\'user@mail.org\', \n        password=\'****\', \n        debug=False\n    )\n    \n    # query execution\n    query = """\n    MATCH (p:Person)-[i]-(m:Movie) where m.id=12\n    return p, i, m\n    limit 100\n    """\n    r = l.run_cypher_query(sourcekey=\'ae46c2f7\', query=query)\n\n    # nodes and edges are transformed before being sent to the visualization \n    r_nodes = [\n        {\n            \'id\': n.data.properties.id, \n            \'data\': {\n                \'geo\': {}\n            }, \n            \'attributes\': {\n                \'layoutable\': True, \n                \'x\': 0, \'y\': 0\n            }\n        } \n        for n in r[\'nodes\']\n    ]\n    r_edges = [\n        {\n            \'id\': e.data.properties.id, \n            \'attributes\': {}\n        } \n        for e in r.edges\n    ]\n    \n    # visualization creation\n    v = l.create_visualization(\n        sourcekey=\'ae46c2f7\', \n        title="Test from API", \n        nodes=r_nodes, \n        edges=r_edges\n    )\n    # server-side auto layouting, in order to spread the nodes\n    l.patch_visualization(\n        sourcekey=\'ae46c2f7\', id=v.id, \n        do_layout=True,\n    )\n    \n    # visualization styles are reset\n    v.design.styles.node = []\n    v.design.styles.edge = []\n    l.patch_visualization(\n        sourcekey=\'ae46c2f7\', id=v.id,     \n        visualization={\'design\': dict(v.design)},\n        force_lock=True\n    )\n\n    # so that they can now be built anew\n    # see https://doc.linkurio.us/server-sdk/latest/apidoc/#api-Visualization-createVisualization\n    # and the links on INodeStyle and IEdgeStyle\n    v.design.styles.node = [\n        { ... }\n    ] \n    v.design.styles.edges = [\n        { ... }\n    ] \n    # design is updated in the visualization\n    # it must be transformed into a dict, as v is a Bunch (from tortilla),\n    # and it may causes all sorts of bad requests responses from Linkurious API\n    l.patch_visualization(\n        sourcekey=\'ae46c2f7\', id=v.id,     \n        visualization={\'design\': dict(v.design)},\n        force_lock=True\n    )\n    \n    # the same can be done for \n    # - visualization filters (v.filters)\n    # - visualization captions (v.nodeFields, v.edgeFields)\n    \n\n## Support\n\nThere is no guaranteed support available, but authors will try to keep up with issues \nand merge proposed solutions into the code base.\n\n## Project Status\nThis project is funded by the European Commission and is currently (2021) under active developement.\n\n## Contributing\nIn order to contribute to this project:\n* verify that python 3.6+ is being used (or use [pyenv](https://github.com/pyenv/pyenv))\n* verify or install [poetry](https://python-poetry.org/), to handle packages and dependencies in a leaner way, \n  with respect to pip and requirements\n* clone the project `git clone git@github.com:openpolis/linkurious.git` \n* install the dependencies in the virtualenv, with `poetry install`,\n  this will also install the dev dependencies\n* develop \n* create a [pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)\n* wait for the maintainers to review and eventually merge your pull request into the main repository\n\n### Testing\nAs this is a tiny utility wrapper around an already tested and quite simple package (tortilla), \nthere are no tests.\n\n## Authors\nGuglielmo Celata - guglielmo@openpolis.it\n\n## Licensing\nThis package is released under an MIT License, see details in the LICENSE.txt file.\n',
    'author': 'guglielmo',
    'author_email': 'guglielmo@openpolis.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/openpolis/linkurious/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
