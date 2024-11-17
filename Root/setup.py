from setuptools import setup

setup(
    name='PeakSeeker',
    version='1.0',
    packages=['game', 'ui', 'backend','assets'], 
    install_requires=[
        'pygame',
        'numpy',
        'perlin-noise', 
        'requests',  
    ],
)