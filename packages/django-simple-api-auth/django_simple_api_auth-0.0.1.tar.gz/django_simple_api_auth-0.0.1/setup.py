from setuptools import setup

tests_require = [
    "pytest-django>=4.4.0",
    "coverage>=5.5"
]
dev_requires = ['twine>=3.4.1'] + tests_require

setup(
    tests_require=tests_require,
    extras_require={"test": tests_require, "dev": dev_requires},
)
