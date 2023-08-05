from setuptools import find_packages, setup
setup(
    name='muapi_client_py',
    packages=find_packages(include=['muapi_client']),
    version='0.1.1',
    description='Client library for Mongo Upload API server',
    author='AlexeiSimonov',
    author_email='sushka2820655@yandex.ru',
    license='MIT',
    install_requires=[
        'requests'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)