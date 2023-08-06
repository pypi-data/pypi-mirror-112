from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
        name='SCA11H',
        version='0.1.0',
        author='Dennis Sitelew',
        author_email='yowidin@gmail.com',
        description='SCA11H Bed Sensor API Helper',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/ihutano/SCA11H',
        project_urls={
            "Bug Tracker": "https://github.com/ihutano/SCA11H/issues",
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        license='MIT',
        packages=find_packages(exclude=('tests',)),
        scripts=[
            'bin/bcg-hostless-api',
        ],
        python_requires=">=3.6",
        zip_safe=False,
)
