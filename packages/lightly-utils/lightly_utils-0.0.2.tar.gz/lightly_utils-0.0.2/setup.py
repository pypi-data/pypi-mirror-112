import setuptools
import sys
import os

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

PATH_ROOT = os.path.dirname(__file__)
builtins.__LIGHTLY_UTILS_SETUP__ = True

import lightly_utils


def load_description(path_dir=PATH_ROOT, filename='DOCS.md'):
    """Load long description from readme in the path_dir/directory.

    """
    with open(os.path.join(path_dir, filename)) as f:
        long_description = f.read()
    return long_description


def load_requirements(path_dir=PATH_ROOT, filename='requirements.txt', comment_char='#'):
    """From pytorch-lightning repo: https://github.com/PyTorchLightning/pytorch-lightning.
       Load requirements from text file in the path_dir/requirements/ directory.

    """
    with open(os.path.join(path_dir, filename), 'r') as file:
        lines = [ln.strip() for ln in file.readlines()]
    reqs = []
    for ln in lines:
        # filer all comments
        if comment_char in ln:
            ln = ln[:ln.index(comment_char)].strip()
        # skip directly installed dependencies
        if ln.startswith('http'):
            continue
        if ln:  # if requirement is not empty
            reqs.append(ln)
    return reqs


if __name__ == '__main__':

    name = lightly_utils.__name__
    version = lightly_utils.__version__
    description = lightly_utils.__doc__

    author = 'Lightly'
    author_email = 'philipp@lightly.ai'
    description = 'A utility package for lightly'

    long_description = load_description()
    python_requires = '>=3.6'
    install_requires = load_requirements()

    packages = [
        'lightly_utils',
        'lightly_utils.image_processing',
    ]

    project_urls = {
        'Homepage': 'https://www.lightly.ai',
        'Web-App': 'https://app.lightly.ai',
        'Documentation': 'https://docs.lightly.ai',
        'Github': 'https://github.com/lightly-ai/lightly',
        'Discord': 'https://discord.gg/xvNJW94',
    }

    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License"
    ]

    setuptools.setup(
        name=name,
        version=version,
        author=author,
        author_email=author_email,
        description=description,
        license='MIT',
        long_description=long_description,
        long_description_content_type='text/markdown',
        install_requires=install_requires,
        python_requires=python_requires,
        packages=packages,
        classifiers=classifiers,
        include_package_data=True,
        project_urls=project_urls,
    )