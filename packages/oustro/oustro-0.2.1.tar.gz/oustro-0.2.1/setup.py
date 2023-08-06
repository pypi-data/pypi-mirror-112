from setuptools import setup, find_packages

VERSION = '0.2.1' 
DESCRIPTION = 'Oustro Package'

# Setting up
setup(
        name="oustro", 
        version=VERSION,
        author="Jacob Thomas",
        author_email="jacobt1206@gmail.com",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=['requests'],

        
        keywords=['python', 'oustro', 'blockchain', 'Oustrochain'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            'Intended Audience :: Developers',
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)