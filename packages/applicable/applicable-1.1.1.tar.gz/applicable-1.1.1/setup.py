from setuptools import find_packages, setup
from pathlib import Path

HERE = Path(__file__).parent
README = (HERE / 'README.md').read_text()

setup(
    name='applicable',
    version='1.1.1',
    description='Test callables without raising exceptions',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/JediChamp178/applicable',
    author='Finn Mason',
    license='GNU General Public License',
    classifiers=[
        'License :: Free for non-commercial use',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    packages=find_packages()
)