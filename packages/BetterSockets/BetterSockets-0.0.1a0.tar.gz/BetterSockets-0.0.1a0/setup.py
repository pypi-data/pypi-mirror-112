from setuptools import setup, find_packages

classifiers = \
    [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers ",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only"
]

setup(
    name="BetterSockets",
    version="0.0.1a",
    description="Better Python sockets and asyncio streams",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Drageast/BetterSockets",
    author="Luca Michael Schmidt",
    author_email="schmidt.lucamichael@gmail.com",
    license="MIT",
    classifiers=classifiers,
    kewords="sockets",
    packages=find_packages()
)
