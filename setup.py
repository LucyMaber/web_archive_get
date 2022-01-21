from setuptools import setup

setup(
    name='web archive get',
    version='0.1.0',    
    description='a tool to find archived web pages from different websites using multiple different services',
#    url='https://github.com/shuds13/pyexample',
    author='William Maber',
    author_email='maberwilliam@gmail.com',
    license='BSD 2-clause',
    packages=['pyexample'],
    install_requires=['aiohttp',
                      'warcio',                     
                      ],

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
