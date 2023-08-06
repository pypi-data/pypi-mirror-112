from distutils.core import setup
import os.path

setup(
  name = 'estdysogoods_bot',
  packages = ['estdysogoods_bot',],
  version = '0.0.0.4',
  description = 'https://www.estdysogoods.com',
  author = 'Nopparat Kumsang (estdysogoods)',       
  author_email = 'estdysogoods@estdysogoods.com',    
  keywords = ['estdysogoods', 'copytrade', 'iqoption', 'Nopparat Kumsang'],
  package_dir={'estdysogoods_bot': 'estdysogoods_bot'},
  package_data={'estdysogoods_bot': ['EDSG_BOT/*.py']},
  install_requires=[
        'iqoption',

    ],
)