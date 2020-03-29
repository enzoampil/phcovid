  
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    install_requires = fh.read().splitlines()

setuptools.setup(
     name='phcovid',  
     version='0.0.2.2',
     author="Lorenzo Ampil",
     author_email="lorenzo.ampil@gmail.com",
     description="Get PH COVID data in only two lines of code!",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/enzoampil/phcovid",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=install_requires,
 )
