from setuptools import setup, Extension

def make_ext(modname, pyxfilename):
    import pysam
    return Extension(
        name=modname,
        sources=[pyxfilename],
        extra_link_args=pysam.get_libraries(),
        include_dirs=pysam.get_include(),
        define_macros=pysam.get_defines()
    )

setup(name='mppysam',
      version='0.1',
      description='Multiprocessing with pysam',
      url='https://github.com/jamesbaye/mppysam',
      author='James Baye',
      author_email='baye.james@gmail.com',
      license='MIT',
      packages=['mppysam'],
      setup_requires=['pysam>=0.15.0'],
      ext_modules=[make_ext("mppysam.dev_pysam", "mppysam/dev_pysam.pyx")],
      install_requires=['pysam>=0.15.0'],
      zip_safe=False)
