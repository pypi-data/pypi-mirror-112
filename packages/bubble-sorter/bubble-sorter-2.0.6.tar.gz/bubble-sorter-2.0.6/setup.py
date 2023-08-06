import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bubble-sorter", 
    version="2.0.6",
    author="Joshua Bode",
    author_email="joshuabode43@gmail.com",
    description="An educational module to demonstrate the efficiency of the bubble sort algorithm. Ideal for small sets of data. Also contains a 'speed_test' function to see how quickly your computer can sort!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MasterJindu/Bubble-Sort-Python",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    
)
