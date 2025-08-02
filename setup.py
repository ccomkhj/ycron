from setuptools import setup, find_packages

setup(
    name="ycron",
    version="0.1.0",
    description="Lightweight YAML-based Cronjob Management",
    author="ccomkhj",
    packages=find_packages(),
    install_requires=[
        "flask",
        "pyyaml",
        "sqlalchemy",
        "croniter",
        "requests",
        "click",
        "pytest",
        "gunicorn",
        "flask_sqlalchemy",
        "flask_cors",
    ],
    entry_points={
        "console_scripts": [
            "ycron = ycron:main",  # Adjust if your main entry is different
        ],
    },
    include_package_data=True,
    python_requires=">=3.7",
)
