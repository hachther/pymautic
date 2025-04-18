from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='pymautic',
    version='0.1.2',
    description='Python client for Mautic',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(include=['pymautic', 'pymautic.*']),
    author='Hachther LLC',
    author_email='contact@hachther.com',
    keywords=['Mautic'],
    url='https://github.com/hachther/pymautic',
    download_url='https://pypi.org/project/pymautic/',
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ]
)
