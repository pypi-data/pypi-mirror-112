import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="custom-logger-cloudcity",
    version="0.0.1",
    packages=setuptools.find_packages(),
    long_description_content_type="text/markdown",
    long_description=long_description,
    python_requires=">=3.9",
    install_requires=[
        "google-cloud-logging ==2.5.0",
        "sentry"
    ],
    url='https://gitlab.com/dqna/custom-logger-cloudcity'
)
