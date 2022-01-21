from setuptools import setup

with open("README.md", "r" ) as fh:
    long_description = fh.read()

setup(
    name='web_archive_get',
    version='0.0.31.2',
    description='a tool to find archived web pages from different websites using multiple different services',
    url='https://github.com/WilliamMaber/web_archive_get/',
    author='Willdor',
    author_email='maberwillliam@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='BSD 2-clause',
    packages=['web_archive_get'],
    install_requires=['aiohttp', 'warcio'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
