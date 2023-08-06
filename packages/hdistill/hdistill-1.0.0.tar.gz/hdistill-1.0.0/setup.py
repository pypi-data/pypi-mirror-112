from setuptools import setup, find_packages
  
with open('requirements.txt') as f:
    requirements = f.readlines()
  
long_description = 'Simple CLI tool used for exploring and parsing HTML documents'
  
setup(
        name ='hdistill',
        version ='1.0.0',
        author ='Seth Taylor',
        author_email ='seth.tales@gmail.com',
        url ='https://github.com/SethTales/hdistill',
        description ='CLI tool for parsing HTML',
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        packages = find_packages(),
        entry_points ={
            'console_scripts': [
                'hdistill = hdistill.main:main'
            ]
        },
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        keywords ='HTML parsing web-scraping',
        install_requires = requirements,
        zip_safe = False
)