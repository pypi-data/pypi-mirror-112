from setuptools import setup,find_packages


setup(
   name='i2db',
   version='1.0',
   description='My Online DB',
   license="MIT",
   long_description=open('README.md','r').read(),
   long_description_content_type='text/x-rst',
   author='Zaid Ali',
   author_email='email@iexi.xyz',
   keywords=['db','database','json'],
    packages=['i2db'],
    install_requires=["requests","json"],
    package_dir={'i2db': 'i2db'},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)