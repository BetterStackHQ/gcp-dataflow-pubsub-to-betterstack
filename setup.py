import setuptools

setuptools.setup(
    name='pubsub-to-betterstack',
    version='0.1.0',
    install_requires=[
        'apache-beam[gcp]>=2.50.0',
        'requests>=2.31.0',
    ],
    packages=setuptools.find_packages(),
) 