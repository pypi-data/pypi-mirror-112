import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ezpredict",
    version="0.0.6",
    author="Samuel Domdey",
    author_email="samuel.domdey@gmail.com",
    description="A small package for convenient predictions on fine-tuned huggingface-models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samueldomdey/ezpredict",
    project_urls={
        "Bug Tracker": "https://github.com/samueldomdey/ezpredict/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)