import setuptools

setuptools.setup(
    name="ghttp",
    version="0.0.1",
    author="Wakie",
    author_email="reg@budist.ru",
    license="MIT",
    description="This is a simple HTTP server based on gevent WSGIServer.",
    url="https://wakie.com",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=2.7",
)
