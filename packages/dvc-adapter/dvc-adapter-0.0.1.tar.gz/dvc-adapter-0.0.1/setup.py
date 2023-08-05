from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = "OpenDataDiscovery DVC Adapter"

setup(
    name='dvc-adapter',
    version='0.0.1',
    author='Provectus team',
    url='https://github.com/opendatadiscovery/odd-dvc-adapter',
    description='OpenDataDiscovery DVC Adapter.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dvc-adapter = adapter:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=requirements,
    zip_safe=False
)