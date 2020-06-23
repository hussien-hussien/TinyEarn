import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TinyEarn-huss", # Replace with your own username
    version="0.0.1",
    author="Hussien Hussien",
    author_email="me@hussien.net",
    description="Simple selenium webscaper to pull earnings data from zacks.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hussien-hussien/TinyEarn",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    platforms=['any'],
    keywords='pandas, earnings report, earnings per share, revenue, finance',
    install_requires=['pandas>=0.24', 'numpy>=1.15',
                      'requests>=2.20', 'multitasking>=0.0.7'],
)