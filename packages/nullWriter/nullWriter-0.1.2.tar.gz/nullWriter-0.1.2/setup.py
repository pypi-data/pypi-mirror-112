from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='nullWriter',
    version='0.1.2',
    description='Hello',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Brendan Doohan',
    author_email='bdoohan@google.com',
    keywords=['nullWriter'],
    url='https://github.com/bdoohan-goog/NullModeler',
    download_url='https://pypi.org/project/NullWriter/'
)

install_requires = [
    'sklearn',
    'numpy'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
    
