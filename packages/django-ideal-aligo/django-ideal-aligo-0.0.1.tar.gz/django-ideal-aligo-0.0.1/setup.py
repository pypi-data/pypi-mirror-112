import setuptools

with open('README.rst', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-ideal-aligo',
    version='0.0.1',
    author='Dongwon Lee',
    author_email='ceo@idealkr.com',
    description='알리고 API 연동을 위한 앱',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://idealkr.com/',
    project_urls={
        'Bug Tracker': 'https://github.com/pypa/sampleproject/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'ideal-aligo'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',
)