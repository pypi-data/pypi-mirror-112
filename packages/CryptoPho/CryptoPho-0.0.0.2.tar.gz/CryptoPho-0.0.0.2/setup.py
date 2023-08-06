from setuptools import setup, find_packages
# from CryptoPho.__init__ import __version__

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name='CryptoPho',
    version="0.0.0.2",
    url='https://github.com/ThePhoenix78/CryptoPho',
    download_url='https://github.com/ThePhoenix78/CryptoPho/tarball/master',
    license='MIT',
    author='ThePhoenix78',
    author_email='thephoenix788@gmail.com',
    description='A random project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=[
        'python',
        'python3',
        'python3.x',
        'ThePhoenix78',
    ],
    install_requires=[
        'setuptools',
    ],
    setup_requires=[
        'wheel'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages()
    # python_requires='>=3.7',
)
