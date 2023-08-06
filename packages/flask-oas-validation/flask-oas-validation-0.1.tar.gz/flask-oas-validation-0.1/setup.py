from distutils.core import setup
setup(
  name = 'flask-oas-validation',
  packages = ['flask-oas-validation'],
  version = '0.1',
  license='GNU GENERAL PUBLIC LICENSE',
  description = 'Test description',
  author = 'Peter Goedeke',
  author_email = 'peterbgoedeke@gmail.com',
  url = 'https://github.com/petergoedeke/flask-oas-validation',
  download_url = 'https://github.com/petergoedeke/flask-oas-validation/archive/v_01.tar.gz',
  keywords = ['flask', 'openapi', 'oas', 'validation', 'automatic'],
  install_requires=[
          'prance',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)