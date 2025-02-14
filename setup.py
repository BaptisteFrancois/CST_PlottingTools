from setuptools import setup, find_packages

setup(
    name='CST_PlottingTools',
    version='0.0.1',
    description='A set of tools for plotting Climate Stress Test results',
    url='https://github.com/BaptisteFrancois/CST_PlottingTools.git',
    author='BaptisteFrancois',
    author_email='BaptisteFrancois51@gmail.com',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas',
        'seaborn',
    ],
    keywords=['python', 'Climate Stress Test', 'CST', 'plotting', 'visualization'],
)