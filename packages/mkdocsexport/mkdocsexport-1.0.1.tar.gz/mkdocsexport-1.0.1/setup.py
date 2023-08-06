from pathlib import Path
from setuptools import setup, find_packages
import os

def read_file(fname):
    "Read a local file"
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = ["mkdocs>=1.1", "jinja2"]
setup_requirements = ["setuptools_scm"]

setup_dir = Path(__file__).parent

setup(
    name='mkdocsexport',
    description="Export documents to a single file. It makes use of a template so the format can be whatever you want (JSON, CSV, One big HTML file, what-ever)",
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs python markdown export',
    url='https://github.com/philips-labs/MkdocsExportPlugin',
    author='Simon de Turck',
    author_email='simon.de.turck@philips.com',
    license='MIT',
    python_requires='>=3.6',
    install_requires=requirements,
    setup_requires=setup_requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    use_scm_version=True,
    include_package_data=True,
    package_data={'export': ['templates/*.template']},
    entry_points={
        'mkdocs.plugins': [
            'mkdocsexport = mkdocsexport.plugin:ExportPlugin'
        ]
    }
)