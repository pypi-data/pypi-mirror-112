#!/usr/bin/env python

from setuptools import setup

setup(
    name='fsleyes-plugin-mrs',

    version='0.0.5',

    description='FSLeyes extension for viewing MRS(I) data formatted as NIfTI-MRS.',

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

    install_requires=['fsleyes>=1.0.10'],

    author='William Clarke, University of Oxford',
    author_email='william.clarke@ndcn.ox.ac.uk'
)
