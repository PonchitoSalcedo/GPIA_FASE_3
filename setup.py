from setuptools import setup, find_packages

setup(
    name="california_housing_mlops",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "xgboost",
        "mlflow",
        "fastapi",
        "uvicorn"
    ],
)
