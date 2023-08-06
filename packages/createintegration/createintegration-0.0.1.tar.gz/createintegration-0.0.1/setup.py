from setuptools import setup

setup(
    name="createintegration",
    version="0.0.1",
    author="Adnan",
    description="Create new integrations",
    long_description="This is a package for creating new integrations",
    install_requires=[],
    packages=['createintegration'],
    entry_points ={
        'console_scripts': [
            'create_integration = createintegration.create_integration:main'
        ]
    },
)

