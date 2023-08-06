from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(name='MerOC',
      version='1.1.5',
      description='Software to download/manipulate netCDF files',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url="https://github.com/carmelosammarco/MerOC",
      author='Carmelo Sammarco',
      author_email='sammarcocarmelo@gmail.com',
      license='gpl-3.0',
      zip_safe=False,
      platforms='OS Independent',
      python_requires='~=3.6',

      include_package_data=True,
      package_data={
        'MerOC': ['DATA/LOGO.gif']

      },

      install_requires=[
        'netCDF4>=1.4.2',
        'ftputil>=3.4',
        'motuclient>=1.8.1',
        'csv342>=1.0.0', 
        'pandas>=0.23.4', 
        'xarray>=0.11.0',
        'shapely>=1.6.4.post1', 
        'fiona>=1.8.4', 
        'cdo>=1.4.0'
      ],
      
      packages=find_packages(),

      entry_points={
        'console_scripts':['MerOC = MerOC.__main__:main']
        
      },

      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3.6',
       ], 

)
