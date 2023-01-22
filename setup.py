import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

version = "0.21.2"

setup(
    name="dyools",
    version=version,
    description="dyools",
    long_description=open('README.txt').read(),
    classifiers=[],
    keywords="dyools",
    author="Mohamed CHERKAOUI",
    author_email="chermed@gmail.com",
    url="https://example.org",
    license="LGPL v3",
    zip_safe=True,
    py_modules=["dyools"],
    include_package_data=True,
    package_dir={},
    packages=["dyools"],
    install_requires=[
        "click",
        "future",
        "pyaml",
        "odoorpc",
        "python-dateutil",
        "prettytable",
        "click",
        "xlsxwriter",
        "xlrd",
        "requests",
        "psutil",
        "faker",
        "lxml",
        "polib",
        "terminaltables",
        "colorclass",
        "dateparser",
        "paramiko",
    ],
    setup_requires=[],
    tests_require=[
        "pytest",
        "pytest-runner",
    ],
    entry_points="""
        [console_scripts]
        ws_agent=dyools:cli_ws_agent
        rpc=dyools:cli_rpc
        tool=dyools:cli_tool
        xml=dyools:cli_xml
        etl=dyools:cli_etl
        po=dyools:cli_po
        sign=dyools:cli_sign
        todo=dyools:cli_todo
        job=dyools:cli_job
        dhelp=dyools:cli_help
        deploy=dyools:cli_deploy
    """,
)
