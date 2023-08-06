import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
LONG_DESCRIPTION = (HERE/'assets/long_description.md').read_text()

setup(
  name = 'pydatastructs',
  version = '1.2.3',
  author = 'Yoshio Hasegawa',
  author_email = 'yoshio.seisuke.hasegawa@gmail.com',
  description = 'A package that contains common data structures',
  long_description = LONG_DESCRIPTION,
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/yoshiohasegawa/python-data-structures',
  download_url = 'https://github.com/yoshiohasegawa/python-data-structures/archive/refs/tags/v1.2.3.tar.gz',
  license='MIT',
  classifiers=[
    "Development Status :: 4 - Beta",
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
    "Topic :: Software Development",
    'Topic :: Software Development :: Build Tools',
	"Topic :: Software Development :: Libraries",
	"Topic :: Software Development :: Libraries :: Python Modules",
  ],
  packages = ['pydatastructs'],
  include_package_data=True,
  install_requires=[
          'typing'
      ],
  keywords = ['Python', 'Data Structures', 'Collections', 'Stack', 'Queue', 'Tree', 'Binary Search Tree', 'Heap', 'Linked List'],
)
