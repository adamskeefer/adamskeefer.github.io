from setuptools import setup, find_packages

setup(
    name="mrfish",
    version="0.1.0",
    description="Mr. Fish File Manager: Automated audio file renaming for student and low budget films",
    packages=find_packages(where="."),
    entry_points={
        "console_scripts": [
            "fish = src.app:main",
        ]
    },
    install_requires=[
        "SpeechRecognition",
    ],
)

