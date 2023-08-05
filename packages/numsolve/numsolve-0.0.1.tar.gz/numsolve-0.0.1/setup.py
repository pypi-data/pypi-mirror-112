from setuptools import setup

setup(
    name="numsolve",
    version='0.0.1',
    description="Numerical Methods to solve various equation",
    keywords=['python', 'numerical methods', 'equation solver'],
    author="Harshal Dupare",
    author_email="<harshal3hd@gmail.com>",
    install_requires=['numpy'],
    py_modules=['numsolve'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    package_dir={'': "src"},
    python_requires=">=3.6",
)