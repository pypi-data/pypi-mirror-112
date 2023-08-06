from setuptools import setup, find_packages, Command
from shutil import rmtree
import os
import sys


def _clearn_folder():
    cur_path = os.path.abspath(os.curdir)

    try:
        print("Start to remove build folders.")
        rmtree(os.path.join(cur_path, 'build'))
        egg_folder = [x for x in os.listdir(cur_path) if x.startswith("auto_ml_cl.")][0]
        rmtree(os.path.join(cur_path, egg_folder))
        rmtree(os.path.join(cur_path, 'dist'))
    except OSError as e:
        pass

_clearn_folder()

# Package meta-data.
NAME = 'auto-ml-cl'
DESCRIPTION = 'Auto machine learning with scikit-learn and TensorFlow framework.'
URL = 'https://github.com/lugq1990/auto-ml-cl'
EMAIL = 'gqianglu@outlook.com'
AUTHOR = 'guangqiang.lu'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = "0.0.16"

REQUIRED = [
        'scikit-learn',
        'pyyaml',
        'tensorflow >= 2.1.0',
        'keras-tuner',
        'google-cloud-storage',
        'lightgbm',
        'xgboost',
        'flask',
        'flask_restful',
        'pandas',
        'numpy'
    ]

path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(path, 'auto_ml')

try:
    with open(os.path.join(path, 'README.md'), encoding='utf-8') as f:
        README = '\n' + f.read()
except FileNotFoundError:
    README = DESCRIPTION


# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = "auto_ml"
    with open(os.path.join(path, project_slug, '__version__.py')) as f:
        print("Get data: ", f.read())
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(path, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.chdir(path)
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIRED,
    package_data={"auto_ml":["*.yml"]},
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)



