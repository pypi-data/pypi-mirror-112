try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

__version__ = '0.0a0.dev1'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='useful_layers',
    packages=find_packages(),
    include_package_data=True,
    version=__version__,
    description="""
Useful Layers is a torch based library containing some experimental,
but useful layers
""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jan Ernsting',
    author_email='j.ernsting@uni-muenster.de',
    url='https://jernsting.github.io/useful_layers/',
    download_url='https://github.com/jernsting/useful_layers/archive/' +
    __version__ + '.tar.gz',
    keywords=['machine learning', 'deep learning', 'experimental', 'science'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    project_urls={
        "Source Code": "https://github.com/jernsting/useful_layers",
        "Documentation": 'https://jernsting.github.io/useful_layers/',
        "Bug Tracker": "https://github.com/jernsting/useful_layers/issues"
    }
)
