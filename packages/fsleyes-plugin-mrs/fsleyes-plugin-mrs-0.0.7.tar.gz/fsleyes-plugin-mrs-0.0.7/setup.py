#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='fsleyes-plugin-mrs',

    version='0.0.7',

    description='FSLeyes extension for viewing MRS(I) data formatted as NIfTI-MRS.',
    author='William Clarke, University of Oxford',
    author_email='william.clarke@ndcn.ox.ac.uk',
    url='https://git.fmrib.ox.ac.uk/wclarke/fsleyes-plugin-mrs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent"],

    python_requires='>=3.7',

    packages=['fsleyes_plugin_mrs'],

    entry_points={

        'fsleyes_views': [
            'MRS view = fsleyes_plugin_mrs.plugin:MRSView',
        ],

        'fsleyes_controls': [
            'NIfTI-MRS = fsleyes_plugin_mrs.plugin:MRSDimControl',
            'MRS control = fsleyes_plugin_mrs.plugin:MRSControlPanel',
            'MRS toolbar = fsleyes_plugin_mrs.plugin:MRSToolBar',
            'FSL-MRS Results = fsleyes_plugin_mrs.results_load:FSLMRSResultsControl',
        ],

        'fsleyes_tools': [
            'Load FSL-MRS fit = fsleyes_plugin_mrs.results_load:FSLFitTool',
        ]


    },

    package_data={'fsleyes_plugin_mrs': ['icons/*.png']},

    install_requires=['fsleyes>=1.0.10']
)
