# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splink_graph']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5.1,<3.0.0', 'numpy==1.19.5', 'pyspark>=2.4', 'scipy>=1.6.0']

setup_kwargs = {
    'name': 'splink-graph',
    'version': '0.4.0',
    'description': 'a small set of graph functions to be used from pySpark on top of networkx and graphframes',
    'long_description': '\n![](https://img.shields.io/badge/spark-%3E%3D2.4.5-orange) ![](https://img.shields.io/badge/pyarrow-%3C%3D%200.14.1-blue)\n\n# splink_graph\n\n\n\n\n![](https://github.com/moj-analytical-services/splink_graph/raw/master/notebooks/splink_graph300x297.png)\n\n---\n\n\n\n`splink_graph` is a small graph utility library in the Apache Spark environment, that works with graph data structures based on the `graphframe` package,\nsuch as the ones created from the outputs of data linking processes (candicate pair results) of ![splink](https://github.com/moj-analytical-services/splink)  \n\n\n\nThe main aim of `splink_graph` is to offer a small set of functions that work on top of established graph packages like `graphframes` and `networkx`  , that can help with\nthe process of data linkage\n\n\n\n\n---\n\n\n## Using Pandas UDFs in Python: prerequisites\n\n\nThis package uses Pandas UDFs for certain functionality.Pandas UDFs are built on top of Apache Arrow and bring \nthe best of both worlds: the ability to define low-overhead, high-performance UDFs entirely in Python.\n\nWith Apache Arrow, it is possible to exchange data directly between JVM and Python driver/executors with near-zero (de)serialization cost.\nHowever there are some things to be aware of if you want to use these functions.\nSince Arrow 0.15.0, a change in the binary IPC format requires an environment variable to be compatible with previous versions of Arrow <= 0.14.1. This is only necessary to do for PySpark users with versions 2.3.x and 2.4.x that have manually upgraded PyArrow to 0.15.0. The following can be added to conf/spark-env.sh to use the legacy Arrow IPC format:\n\n    ARROW_PRE_0_15_IPC_FORMAT=1`\n\nAnother way is to put the following on spark .config\n\n    .config("spark.sql.execution.arrow.pyspark.enabled", "true")\n    .config("spark.executorEnv.ARROW_PRE_0_15_IPC_FORMAT", "1")\n\n\nThis will instruct PyArrow >= 0.15.0 to use the legacy IPC format with the older Arrow Java that is in Spark 2.3.x and 2.4.x. Not setting this environment variable will lead to a similar error as described in [SPARK-29367](https://issues.apache.org/jira/browse/SPARK-29367) when running pandas_udfs or toPandas() with Arrow enabled.\n\n\nSo all in all : either PyArrow needs to be at most in version 0.14.1 or if that cannot happen the above settings need to be be active.\n\n\n\n\n\n\n---\n\n\n## Terminology\n\nLike any discipline, graphs come with their own set of nomenclature. \nThe following descriptions are intentionally simplified—more mathematically rigorous definitions can be found in any graph theory textbook.\n\n`Graph` \n\n    — A data structure G = (V, E) where V and E are a set of vertices/nodes and edges.\n\n`Vertex/Node` \n\n    — Represents a single entity such as a person or an object,\n\n`Edge` \n\n    — Represents a relationship between two vertices (e.g., are these two vertices friends on a social network?).\n\n`Directed Graph vs. Undirected Graph` \n\n    — Denotes whether the relationship represented by edges is symmetric or not \n\n`Weighted vs Unweighted Graph` \n\n     — In weighted graphs edges have a weight that could represent cost of traversing or a similarity score or a distance score\n\n     — In unweighted graphs edges have no weight and simply show connections . example: course prerequisites\n\n`Subgraph` \n\n    — A set of vertices and edges that are a subset of the full graph\'s vertices and edges.\n\n`Degree` \n    \n    — A vertex/node measurement quantifying the number of connected edges \n\n`Connected Component` \n\n    — A strongly connected subgraph, meaning that every vertex can reach the other vertices in the subgraph.\n\n`Shortest Path` \n    \n    — The lowest number of edges required to traverse between two specific vertices/nodes.\n\n\n\n\n\n---\n\n## Contributing\n\nFeel free to contribute by \n\n * Forking the repository to suggest a change, and/or\n * Starting an issue.',
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
