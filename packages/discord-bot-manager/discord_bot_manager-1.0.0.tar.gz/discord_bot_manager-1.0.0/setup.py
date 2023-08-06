from distutils.core import setup

from setuptools import find_packages

setup(
    name='discord_bot_manager',  # How you named your package folder (MyLib)
    packages=find_packages(exclude=("tests",)),
    version='1.0.0',
    license='MIT',
    description='TYPE YOUR DESCRIPTION HERE',
    author='YOUR NAME',
    author_email='vaskrneup@gmail.com',
    url='https://github.com/vaskrneup/DiscordBot',
    keywords=["discord", "bot", "manager"],
    install_requires=[
        "aiohttp",
        "async-timeout",
        "attrs",
        "certifi",
        "chardet",
        "discord",
        "discord.py",
        "idna",
        "multidict",
        "requests",
        "typing-extensions",
        "urllib3",
        "yarl",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
