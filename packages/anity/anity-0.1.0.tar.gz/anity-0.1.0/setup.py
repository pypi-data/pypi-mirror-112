import pathlib
from setuptools import setup, find_packages

PKG = pathlib.Path(__file__).parent
README = (PKG / 'README.md').read_text()

setup(
    name='anity',
    version='0.1.0',
    description='Deploy monitor test suites in anity.io',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://anity.io',
    author='Anity',
    author_email='info@anity.io',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'anity = anity.__main__:cli',
        ],
    },
)
