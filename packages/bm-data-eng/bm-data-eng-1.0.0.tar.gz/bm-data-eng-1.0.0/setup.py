from setuptools import setup

setup(
    name="bm-data-eng",
    version="1.0.0",
    description="BM Data Eng lib to transfer files from S3 to GCS, transform them and "
    "load them to BQ",
    author="Thomas Pilewicz",
    packages=["bm_data_eng"],
    include_package_data=True,
    install_requires=["pandas==1.1.5", "pyarrow==4.0.1"]
)
