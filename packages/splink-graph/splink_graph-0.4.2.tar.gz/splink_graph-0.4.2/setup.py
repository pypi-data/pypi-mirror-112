# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splink_graph']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5.1,<3.0.0', 'numpy==1.19.5', 'scipy>=1.6.0']

setup_kwargs = {
    'name': 'splink-graph',
    'version': '0.4.2',
    'description': 'a small set of graph functions to be used from pySpark on top of networkx and graphframes',
    'long_description': '\n![](https://img.shields.io/badge/spark-%3E%3D2.4.5-orange) ![](https://img.shields.io/badge/pyarrow-%3C%3D%200.14.1-blue) ![](https://img.shields.io/github/languages/top/moj-analytical-services/splink_graph) ![](https://img.shields.io/pypi/v/splink_graph)\n\n# splink_graph\n\n\n\n\n![](https://github.com/moj-analytical-services/splink_graph/raw/master/notebooks/splink_graph300x297.png)\n\n---\n\n\n`splink_graph` is a small graph utility library meant to be used in the Apache Spark environment, that works with graph data structures \nsuch as the ones created from the outputs of data linking processes (candicate pair results) of ![splink](https://github.com/moj-analytical-services/splink) \n\nThe main aim of `splink_graph` is to offer a small set of functions that work on top of established graph packages like `graphframes` and `networkx`  , that can help with the process of graph analysis of the output of probabilistic data linkage tools.\n\n---\n\n## Functionality offered\n\nFor a primer on the terminology used please look at TERMINOLOGY.md file in this repo\n\n\n####  Cluster metrics\n\nCluster metrics usually have as an input a spark edgelist dataframe that also includes the component_id (cluster_id) where the edge is in.\nThe output is a row of one or more metrics per cluster\n\nCluster metrics currently offered: \n\n- diameter\n- transitivity\n- cluster triangle clustering coeff\n- cluster square clustering coeff\n- cluster node connectivity\n- edge connectivity\n- cluster efficiency\n- cluster modularity\n- cluster avg edge betweenness\n- cluster weisfeiler lehman graphhash\n\nCluster metrics are really helpful at finding the needle (of for example clusters with possible linking errors) in the \nhaystack (whole set of clusters after the data linking process)\n\n---\n\n####  Node metrics\n\nNode metrics  have as an input a spark edgelist dataframe that also includes the component_id (cluster_id) where the edge is in.\nThe output is a row of one or more metrics per node\n\nNode metrics curretnly offered: \n\n- Eigenvector Centrality \n- Harmonic centrality\n\n---\n\n####  Edge metrics\n\nEdge metrics  have as an input a spark edgelist dataframe that also includes the component_id (cluster_id) where the edge is in.\nThe output is a row of one or more metrics per edge\n\nEdge metrics curretnly offered: \n\n- Edge Betweeness\n- Bridge Edges\n\n\n---\n\n\n## Contributing\n\nFeel free to contribute by \n\n * Forking the repository to suggest a change, and/or\n * Starting an issue.\n',
    'author': 'Theodore Manassis',
    'author_email': 'theodore.manassis@digital.justice.gov.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moj-analytical-services/splink_graph',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
