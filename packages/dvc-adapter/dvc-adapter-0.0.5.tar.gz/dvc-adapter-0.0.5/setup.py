from setuptools import setup, find_packages

long_description = "OpenDataDiscovery DVC Adapter"

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='dvc-adapter',
    version='0.0.5',
    author='Provectus team',
    url='https://github.com/opendatadiscovery/odd-dvc-adapter',
    description='OpenDataDiscovery DVC Adapter.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    install_requires = requirements,
    entry_points={
        'console_scripts': [
            'dvc-adapter = dvc_adapter.adapter:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    zip_safe=False
)