from setuptools import setup, find_packages
setup(name='notification_services',
version='0.1',
packages=find_packages(),
install_requires=['requests', 'flatten_dict', 'abc', ]
)