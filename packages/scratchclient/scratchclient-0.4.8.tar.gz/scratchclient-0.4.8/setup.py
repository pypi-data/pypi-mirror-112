import setuptools
from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name = 'scratchclient',
  packages = ['scratchclient'],
  version = '0.4.8',
  license='MIT',
  description = 'A scratch API wrapper for Python.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'CubeyTheCube',
  author_email = 'turtles142857@gmail.com',
  url = 'https://github.com/CubeyTheCube/scratchclient',
  download_url = 'https://github.com/CubeyTheCube/scratchclient/archive/v_04.8.tar.gz',
  keywords = ['scratch', 'api'],
  install_requires=[
          'requests',
          'websocket-client',
          'numpy',
          'wsaccel',
          'pymitter'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)