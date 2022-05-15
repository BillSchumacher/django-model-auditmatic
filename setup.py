from os.path import exists

from setuptools import find_packages, setup

setup(
    name="django-model-auditmatic",
    author="Bill Schumacher",
    author_email="william.schumacher@gmail.com",
    packages=find_packages(),
    scripts=[],
    url="https://github.com/BillSchumacher/django-model-auditmatic",
    license="MIT",
    description="Audit support for Django models using PostgreSQL "
    "triggers and stored procedures.",
    long_description=open("README.md").read() if exists("README.md") else "",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=["django", "psycopg2"],
    version="0.0.3",
    zip_safe=False,
)
