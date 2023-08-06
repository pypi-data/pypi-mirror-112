import setuptools

setuptools.setup(
    name="hardware-api-client",
    version="0.0.4",
    author="Andre Renaud",
    author_email="arenaud@designa-electronics.com",
    description="Python interface for testing against Hardware-API.com attached systems",
    url="https://hardware-api.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requests=[
        "requests",
        "websocket",
        "xmodem",
    ],
)
