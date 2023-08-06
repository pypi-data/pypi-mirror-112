from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = "csgo_handler",
    packages = [
        "csgo_handler"
    ],
    platforms = [
        "linux",
    ],
    version = "1.0.1",
    license = "AGPLv3",
    description = "Daemon to run a program when CS:GO starts and stops",
    long_description = long_description,
    long_description_content_type="text/markdown",
    author = "Alex Wicks",
    author_email = "alex@awicks.io",
    url = "https://gitlab.com/aw1cks/csgo_handler",
    download_url = "https://gitlab.com/aw1cks/csgo_handler",
    scripts = [
        "bin/csgo_handler",
    ],
    keywords = [
        "csgo",
    ],
    install_requires = [
        "python-daemon",
        "inotify",
    ],
    python_requires = ">=3.6",
    package_dir={
        "csgo_handler": "src"
    },
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Communications :: Chat",
    ],
)
