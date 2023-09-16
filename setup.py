from setuptools import setup, find_packages

setup(
    name='client_python_m2p',
    version='1.0.1',
    url='https://github.com/easytopic-project/client-python-m2p',
    license='MIT License',
    author='Bruno Jucá',
    author_email='brunoolijuca@gmail.com',
    keywords='python client for m2p',
    description='Python client for M2P',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['pika'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)