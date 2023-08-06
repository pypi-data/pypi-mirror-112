# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='plumbline',  # Required
    version='0.0.2',  # Required
    description='Python for comparing EPT and DEM data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hobu/plumbline',
    author='Howard Butler',
    author_email='howard@hobu.co',
    classifiers=[  \
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],

    packages=find_packages(),  # Required
    python_requires='>=3.8',

    install_requires=['pdal','matplotlib', 'ept-python','Shapely', 'rasterio','dask', 'pyproj'],  # Optional

#     entry_points={  # Optional
#         'console_scripts': [
#             'plumbline2=plumbline.plumbline.main',
#         ],
#     },

)

