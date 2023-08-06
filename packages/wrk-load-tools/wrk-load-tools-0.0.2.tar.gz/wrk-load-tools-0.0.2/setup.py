from setuptools import setup
from wrktoolbox import version


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='wrk-load-tools',
      version=version,
      description='A tool to run wrk/wrk2 benchmarks and store their output.',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Operating System :: Unix'
      ],
      url='https://github.com/kishorekumar-kk/wrktoolbox',
      author = 'Kishore Kumar',
      author_email = 'mailtokishorekumar.s@gmail.com',
      keywords='wrk runner benchmarks load performance tests',
      license='MIT',
      packages=['wrktoolbox',
                'wrktoolbox.stores',
                'wrktoolbox.plugins',
                'wrktoolbox.goals',
                'wrktoolbox.commands',
                'wrktoolbox.reports',
                'wrktoolbox.results',
                'wrktoolbox.results.importers'],
      install_requires=['pyparsing',
                        'rocore',
                        'roconfiguration',
                        'click',
                        'certifi'],
      include_package_data=True,
      zip_safe=False,
      entry_points="""
      [console_scripts]
      wrktoolbox=wrktoolbox.main:main
      """)
