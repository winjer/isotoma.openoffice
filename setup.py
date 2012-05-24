from setuptools import setup, find_packages

version = '0.0.4.dev0'

setup(
    name = 'isotoma.openoffice',
    version = version,
    description = "Utility for accessing openoffice",
    long_description = open("README.rst").read() + "\n" + \
                       open("CHANGES.txt").read(),
    url = "http://pypi.python.org/pypi/isotoma.openoffice",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Software Distribution",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords = "openoffice pdf",
    author = "Doug Winter",
    author_email = "doug.winter@isotoma.com",
    license="Apache Software License",
    packages = find_packages(exclude=['ez_setup']),
    namespace_packages = ['isotoma'],
    include_package_data = True,
    zip_safe = False,
    install_requires = [
    ],
)
