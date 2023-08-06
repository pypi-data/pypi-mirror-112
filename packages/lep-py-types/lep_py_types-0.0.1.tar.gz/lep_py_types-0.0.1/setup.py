import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
  name = 'lep_py_types',         
  packages=find_packages('.', exclude=['test']), 
  version = '0.0.1',      
  license='MIT',       
  description = 'Lepsta events protobuf types',   
  author = 'Lepsta Inc',                   
  author_email = 'damilola@lepsta.com',      
  url = 'https://github.com/lepsta/types',   
  download_url = 'https://github.com/lepsta/types/archive/refs/tags/v0.0.1.tar.gz',    
  keywords = ['Types', 'Protobuf'], 
  install_requires=['protobuf'],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    # 'Intended Audience :: Lepsta Developer',      
    'Programming Language :: Python :: 3.9',
  ],
  include_package_data=True
)