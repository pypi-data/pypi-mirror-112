from setuptools import setup, find_packages

VERSION = '0.0.8'
DESCRIPTION = 'Capitalism API wrapper in Python'

# Setting up
setup(name='capapi',
      author='drapes',
      author_email='lildrapesbusiness@gmail.com',
      url='https://github.com/drapespy/CapAPI',
      version=VERSION,
      packages=find_packages(),
      license='MIT',
      long_description=open("README.md").read(),
      long_description_content_type="text/markdown",
      description=DESCRIPTION,
      install_requires=['requests'],
      python_requires='>=3.5.3',
      keywords = ['python', 'capitalism', 'api wrapper', 'api', 'wrapper', 'capi', 'capi.py'],
      classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)