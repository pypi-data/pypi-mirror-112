import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='lionhandler',  
     version='0.3',
     scripts=['client'] ,
     author="Saulo Leão",
     author_email="sleaojr@gmail.com",
     description="A client application for handling logging sending to a server",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/thiagolrpinho/loghandler-client",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )