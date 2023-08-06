# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tysserand']

package_data = \
{'': ['*']}

install_requires = \
['dask',
 'hdbscan',
 'ipykernel',
 'matplotlib',
 'napari',
 'numpy',
 'opencv-python',
 'pathlib',
 'qtconsole',
 'scikit-image',
 'scikit-learn',
 'scipy',
 'seaborn',
 'umap-learn']

setup_kwargs = {
    'name': 'tysserand',
    'version': '0.3.0',
    'description': 'Fast and accurate spatial networks reconstruction.',
    'long_description': '# tysserand\n\nFast and accurate spatial networks reconstruction.\n\n![](./images/tysserand_main_figure.png)\n\n*tysserand* is a Python library to reconstruct spatial networks from spatially resolved omics experiments. It is intended as a common tool where the bioinformatics community can add new methods to reconstruct networks, choose appropriate parameters, clean resulting networks and pipe data to other libraries.  \nYou can find the article and supplementary information on [Bioinformatics](https://doi.org/10.1093/bioinformatics/btab490), and the freely available preprint (same text!) is on [BioRxiv](https://www.biorxiv.org/content/10.1101/2020.11.16.385377v2).  \nA turorial is available [here](./examples/02-tutorial.ipynb)\n\n*tysserand* is fast: it is 50 to more than 120 times faster than PySAL.  \n*tysserand* is accurate: it implements the best performing methods, tested on simulated and real bioimages.\n*tysserand* is user friendly and interactive: it integrates tools to choose appropriate parameters and facilitates the use of napari-based interactive image visualization and network annotation.\n*tysserand* is modular and opened to contributions: if you have an idea on how to improve reconstruction methods, create a particular one for a specific case, or make them even faster, join us!\n\n## Installation\n\nSimply do\n```bash\npip install tysserand\n```\n\nTo install a dedicated environment, if you already have conda you can use Mamba to do it pretty quickly:\n```bash\nconda install mamba -n base -c conda-forge\nmamba env create --file conda_env_spatial-networks.yml\n```\nBut ideally use pyenv + virtualenvs + poetry for better reproducibility and full open source stack (detailedexplanations coming soon).\n\n## Implemented methods\n\n![Set of nodes](./images/publication_figures/mIF-nodes_positions.png)\n\n### Delaunay triangulation\n\nThis method builds virtual cells centered arround each node and contacting each other to fully tile the space occupyied by the nodes. Edges are drawn between the nodes of contacting tiles.\n\n![Edge lengths with *Delaunay* reconstruction](./images/publication_figures/mIF-Delaunay_distances.png)  \n![Trimmed network](./images/publication_figures/mIF-Delaunay_network.png)  \n![Network overlay on original tissue image](./images/publication_figures/mIF-Delaunay_superimposed.png)  \n\n### k-nearest neighbors\n\nEach node is linked with its k nearest neighbors. It is the most common method used in single cell publications, althought it produces artifacts well visible on simple 2D networks.\n\n![Edge lengths with *k-nearest neighbors* reconstruction](./images/publication_figures/mIF-knn_distances.png)\n\n### radial distance neighbors\n\nEach node is linked to nodes closer than a threshold distance D, that is to say each node is linked to all nodes in a circle of radius D.\n\n![Edge lengths with *radial distance neighbors* reconstruction](./images/publication_figures/mIF-rdn_distances.png)\n\n### Area contact\n\nNodes are the center of detected objects (like after cell segmentation) and they are linked if their respective areas are in contact or closer than a given distance threshold.  \nA parallelized version is implemented with the Dask library.\n\n![*Contacting areas* reconstruction](./images/publication_figures/simulated_segmentation_image_size-600_hole_proba-0.1_noise_sigma-10.0_objects_network.png)\n\n### Area contact *and* k-nearest neighbors\n\nAreas are linked if they are in contact or closer than a given distance. Then, the remaining non connected areas are connected with their nearest neighbors.\n',
    'author': 'Alexis Coullomb',
    'author_email': 'alexis.coullomb.pro@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
