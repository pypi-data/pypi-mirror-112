import setuptools


setuptools.setup(
    name="nerdpool-client",
    version="0.0.1",
    author="Peter Andorfer",
    author_email="peter.andorfer@oeaw.ac.at",
    description="A client for Nerdpool-Api",
    url="https://github.com/acdh-oeaw/nerdpool-client",
    license='MIT',
    packages=['nerdpool_client'],
    zip_safe=False,
    install_requires=[
        'requests',
    ],
)
