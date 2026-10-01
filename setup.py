from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(name='multinets',
      version='0.1.0',
      description='Multilevel Network Analysis',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/neylsoncrepalde/multinets-py',
      project_urls={
          'Documentation': 'https://neylsoncrepalde.github.io/multinets-py/',
          'R package': 'https://github.com/neylsoncrepalde/multinets'
      },
      author='Neylson Crepalde',
      author_email='neylsoncrepalde@gmail.com',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Sociology',
        'Typing :: Typed'
      ],
      keywords='multilevel networks social network analysis igraph networkx',
      license_expression='GPL-3.0-only',
      license_files=['LICENSE.md'],
      packages=['multinets'],
      package_dir={'': 'src'},
      package_data={'multinets': ['data/*.graphml', 'py.typed']},
      zip_safe=False,
      install_requires=[
          'igraph>=0.11.5',  # to_networkx() is broken for multigraphs before 0.11.5
          'numpy>=1.22'
      ],
      extras_require={
          'networkx': ['networkx>=3.0'],
          'plot': ['matplotlib>=3.6'],
          'test': ['pytest>=7', 'networkx>=3.0', 'matplotlib>=3.6'],
          'docs': [
              'sphinx>=9.1',
              'pydata-sphinx-theme>=0.22',
              'myst-nb>=1.4',
              'sphinx-design>=0.7',
              'sphinx-copybutton>=0.5.2',
              'networkx>=3.0',
              'matplotlib>=3.6'
          ]
      },
      python_requires='>=3.9')
