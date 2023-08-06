# Lib
from setuptools import setup, find_packages
exec(open('methylsuite/version.py').read())

setup(
    name='methylsuite',
    version=__version__,
    description='Python-based Illumina methylation array processing and analysis software composite package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    project_urls = {
        "Funding": "https://FOXOBioScience.com/"
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Framework :: Jupyter',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Financial and Insurance Industry',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
      ],
    keywords='methylation dna data processing epigenetics illumina',
    url="https://life-epigenetics-methylprep.readthedocs-hosted.com/en/latest/",
    license='MIT',
    author='FOXO Bioscience',
    author_email='info@FOXOBioScience.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'statsmodels',
        'tqdm',
        'bs4',
        'lxml',
        'methylprep',
        'methylcheck',
        'methylize',
        'requests',
        'matplotlib',
        'seaborn',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest','pytest_mock']
)
