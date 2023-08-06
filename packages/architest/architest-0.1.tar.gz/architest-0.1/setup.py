from setuptools import setup
setup(
  name = 'architest',
  packages = ['architest'],
  version = '0.1',
  license='MIT',
  description = "Architest allows you to check your project's structure conformity to initial architecture",
  author = 'Vladimir Semenov',
  author_email = 'subatiq@gmail.com',
  url = 'https://github.com/VASemenov/architest',
  download_url = 'https://github.com/VASemenov/architest/archive/refs/tags/0.1.tar.gz',
  keywords = ['architest', 'static', 'test', 'architecture', 'design'],
  install_requires=[
          'pyyaml',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)