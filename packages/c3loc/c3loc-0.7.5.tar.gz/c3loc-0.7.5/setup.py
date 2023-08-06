from setuptools import find_packages, setup

def get_version_and_cmdclass(package_path):
    """Load version.py module without importing the whole package.

    Template code from miniver
    """
    import os
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location("version", os.path.join(package_path, "_version.py"))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__, module.cmdclass


version, cmdclass = get_version_and_cmdclass("src/c3loc")

setup(
    name='c3loc',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,
    cmdclass=cmdclass,
    description='C3 Enhanced Proximity Location Services',
    url='https://gitlab.com/C3Wireless/c3loc',
    author='C3 Wireless',
    author_email='support@c3wireless.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='c3 c3wireless btle beacon ibeacon',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=[
        'alembic',
        'asyncpg',
        'aiohttp',
        'aiohttp-cors',
        'aiohttp-jinja2',
        'automat',
        'click',
        'marshmallow',
        'protobuf',
        'psycopg2',
        'python-lzo',
        'cryptography',
        'python-dateutil',
        'pytz',
        'jinja2',
        'sqlalchemy',
        'sqlalchemy-utils',
        'fastapi',
        'pydantic',
        'uvicorn',
        # 'uvloop'
    ],
    extras_require={
        'test': ['pytest', 'pytest-cov', 'pytest-asyncio', 'hypothesis',
                 'aiosqlite', 'httpx', 'mypy', 'gevent', 'coverage'],
    },
    entry_points={
        'console_scripts': [
            'c3loc_ingest=c3loc.ingest.main:main',
            'c3loc_api=c3loc.api.main:main',
            'c3loc_api2=c3loc.api2.main:main'
        ],
    },
    package_data={'c3loc': ['static/*', 'templates/*', 'alembic.ini', 'alembic/*', 'alembic/versions/*']}
)
