from setuptools import setup

setup(
    name="igraph",
    version="0.1.13",
    description="View graph data structures in the IPython notebook (deprecated).",
    url="http://github.com/patrickfuller/jgraph/",
    license="MIT",
    author="Patrick Fuller, Tamas Nepusz",
    author_email="patrickfuller@gmail.com, ntamas@gmail.com",
    package_dir={'igraph': 'igraph'},
    packages=['igraph'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Framework :: IPython',
        'Topic :: Education :: Computer Aided Instruction (CAI)'
    ]
)
