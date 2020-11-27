from setuptools import setup

setup(name='mppysam',
      version='0.1',
      description='Multiprocessing with pysam',
      url='https://github.com/jamesbaye/mppysam',
      author='James Baye',
      author_email='baye.james@gmail.com',
      license='MIT',
      packages=['mppysam'],
      install_requires=[
          'pysam>=0.15.0'
      ],
      zip_safe=False)
