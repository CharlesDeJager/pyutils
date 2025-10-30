from setuptools import setup, find_packages

setup(
    name='my_python_project',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # Add your project's dependencies here
    ],
    entry_points={
        'console_scripts': [
            'my-command=my_package.cli:main',
        ],
    },
)