from setuptools import setup

setup(
    name = 'cendas',
    version = '0.0.3',
    description = 'Cendas is a new pandas-based software library optimized for analyzing data provided by U.S. government agencies.',
    py_modules = ["cendas"],
    package_dir = {'': 'src'},

    install_requires = [
        'pandas'
    ],

    url = 'https://github.com/justinkim668/cendas',
    author = 'Justin Kim',
    author_email = 'jtk2141@columbia.edu'
)
