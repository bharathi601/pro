from setuptools import setup, find_packages

setup(
    name="SmartSolutionx",  # Name of your package
    version="0.1.0",
    author="Your Name",
    author_email="bharathis220106@gmail.com",
    description="A collection of innovative tech and academic projects by SmartSolutionx.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SmartSolutionx",  # Your GitHub repo
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Software Development :: Embedded Systems",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Example: "numpy", "micropython-mpu6050", etc.
    ],
    include_package_data=True,
)
