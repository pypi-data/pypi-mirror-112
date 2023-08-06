from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Best practices for Docker file'
LONG_DESCRIPTION = 'Best practices for Docker file'

# Setting up
setup(
        name="docker_checks", 
        version=VERSION,
        author="Pranav Bhatia",
        author_email="<prav10194@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        include_package_data=True,
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)