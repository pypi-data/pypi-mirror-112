from setuptools import setup

packages_wanpy = [
    'exwanpy',
]

# for release package: python setup.py sdist
setup(
    name='example_wanpy',
    version=0.2,
    include_package_data=True,
    packages=packages_wanpy,
    license='GPL v3',
)
