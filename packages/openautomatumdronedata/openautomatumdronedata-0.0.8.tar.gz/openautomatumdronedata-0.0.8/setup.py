from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='openautomatumdronedata',
    version='0.0.8',    
    description='A utility package for the open automatum drone dataset',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://www.automatum-data.com',  # Optional
    project_urls={  # Optional
        'Bug Reports': 'https://bitbucket.org/automatum/open.automatum.dronedata/issues?status=new&status=open',
        'Documentation': 'https://openautomatumdronedata.readthedocs.io/en/latest/',
        'Source': 'https://bitbucket.org/automatum/open.automatum.dronedata/src/master/',
    },

    author='Peter Zechel',
    author_email='peter@automatum-data.com',
    license='CC-BY-SA',
    packages=['openautomatumdronedata'],
    install_requires=['bokeh > 2.0.0'],
    setup_requires=['bokeh > 2.0.0'],
    entry_points={
        "console_scripts": [
            "automatum_vis = openautomatumdronedata.automatumBokehSever:main"
        ]
    },
    classifiers=[
         'Development Status :: 2 - Pre-Alpha',
         'Intended Audience :: Science/Research',
         'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',  
         'Operating System :: POSIX :: Linux',
         'Operating System :: MacOS', 
         'Operating System :: Microsoft :: Windows',
         'Programming Language :: Python :: 3',
    ],
)