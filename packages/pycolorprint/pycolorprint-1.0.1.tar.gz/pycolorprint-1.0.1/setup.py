from setuptools import setup, find_packages

VERSION = '1.0.1' 
DESCRIPTION = 'Colorful pretty printer for python!'
LONG_DESCRIPTION = 'A python pretty printer that uses ANSI characters to make terminal output colorful.\n\n\
                    (5/10/2021) cprint_iter now returns the ANSI colored string that is printed to console.\n\n\
                    (7/5/2021) cprint_iter has been deprecated, cprint can handle all var types now and all ANSI commands, text colors, and highlight colors are all exported in __init__.py for use outside of cprint\
                    (7/6/2021) cprint now has the optional color arg that can change the color or highlight of non iterable primitives when printed and returned'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pycolorprint",
        version=VERSION,
        author="Alexander Steffen",
        author_email="alexsteffen55@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package.
        
        keywords=['python', 'pretty printer', 'print', 'colorful', 'color', 'color printer', 'color print'],
        classifiers= [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)

# cmds:
# python setup.py sdist bdist_wheel
# twine upload dist/*