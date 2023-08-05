
#from distutils.core import setup, find_packages
from setuptools import setup, find_packages
setup(
  name = 'Electroplot',         # How you named your package folder (MyLib)
  packages = find_packages(include=['Electroplot', 'Electroplot.*']), 
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Handling TIFF files and figure generation from timelapse experiments.',   # Give a short description about your library
  author = 'Conor Edwards',                   # Type in your name
  author_email = 'conorlo@hotmail.co.uk',      # Type in your E-Mail
  url = 'https://github.com/ConorEd/',   # Provide either the link to your github or to your website
  #download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['IMAGE ANALYSIS', 'TIFF', 'TIMELAPSE'],   # Keywords that define your package best
  install_requires=[            
          'numpy',
          'moviepy',
          'tifffile',
          'matplotlib',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)