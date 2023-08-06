# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 15:35:27 2021

@author: Kardi
"""

from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'IdealFlowNetwork',        
  packages = ['IdealFlowNetwork'],   
  version = '1.0.2',      
  license='GNU General Public License v3.0',   
  description = 'Ideal Flow Network Python Library',  
  author = 'Kardi Teknomo',                  
  author_email = 'teknomo@gmail.com',     
  url = 'http://people.revoledu.com/kardi/',   
  download_url = 'https://github.com/teknomo/IdealFlowNetwork/blob/master/dist/IdealFlowNetwork-1.0.1.tar.gz',
  keywords = ['IFN', 'Markov', 'irreducible', 'premagic'],
  long_description=long_description,
  long_description_content_type="text/x-rst",
  install_requires=[           
          'numpy',
          'pandas',
      ],
  entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
  classifiers=[
    'Development Status :: 5 - Production/Stable',    
    'Intended Audience :: Developers', 
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Topic :: Education',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Software Development :: Libraries',
    'License :: Free for non-commercial use',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
    
  ],
)