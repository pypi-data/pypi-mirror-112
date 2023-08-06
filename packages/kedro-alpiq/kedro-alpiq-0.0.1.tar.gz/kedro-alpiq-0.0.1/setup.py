from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name="kedro-alpiq",
    version="0.0.1",
    author="Lucas Jamar",
    author_email="lucas.jamar@alpiq.com",
    url="https://alpiq.com",
    packages=["kedro_alpiq"],
    license="Commercial",
    description="A Public stub for kedro-alpiq by Alpiq",
    long_description=readme,
    long_description_content_type='text/markdown',
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)
