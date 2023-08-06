from setuptools import find_packages, setup


PACKAGES = find_packages(include=['pysdsbapi'])

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pysdsbapi',
    version='0.6.0',
    author='mlad_Blum',
    description='Experimental library for interacting with the experimental sds bridge api.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=PACKAGES,
    install_requires=['aiohttp==3.7.4'],
    python_requires=">=3.6",
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)