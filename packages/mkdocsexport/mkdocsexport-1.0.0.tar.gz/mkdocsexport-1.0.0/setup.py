from setuptools import setup, find_packages
import os

def read_file(fname):
    "Read a local file"
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='mkdocsexport',
    version='1.0.0',
    description="Export documents to a single file. It makes use of a template so the format can be whatever you want (JSON, CSV, One big HTML file, what-ever)",
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs python markdown export',
    url='https://github.com/philips-labs/MkdocsExportPlugin',
    author='Simon de Turck',
    author_email='simon.de.turck@philips.com',
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
        'mkdocs>=1.1',
        'jinja2',
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={'export': ['templates/*.template']},
    entry_points={
        'mkdocs.plugins': [
            'mkdocsexport = mkdocsexport.plugin:ExportPlugin'
        ]
    }
)