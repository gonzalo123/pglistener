from setuptools import setup

with open("README_PGLISTENER.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name="pglistener-gonzalo123",
    version="1.0.1",
    author="Gonzalo Ayuso",
    author_email="gonzalo123@gmail.com",
    description="psycopg2 db listener",
    long_description=long_description,
    license='MIT',
    long_description_content_type="text/markdown",
    keywords=['psycopg2'],
    url="https://github.com/gonzalo123/pglistener",
    packages=['pg_listener'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)

install_requires = [
    'psycopg2-binary>=2.8.6'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
