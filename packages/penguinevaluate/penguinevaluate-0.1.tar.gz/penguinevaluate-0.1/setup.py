from setuptools import setup

setup(name='penguinevaluate',
      version='0.1',
      description='assesses books sold after publicity or marketing',
      url='https://github.com/puk/marketing-evaluation',
      author='Jessica Harris',
      author_email='jharris2@penguinrandomhouse.co.uk',
      license='?',
      include_package_data=True,
      packages=['penguinevaluate'],
      install_requires=['causalimpact',
                        'numpy',
                        'pandas',
                        'tslearn',
                        'sklearn',
        ],
      zip_safe=False)