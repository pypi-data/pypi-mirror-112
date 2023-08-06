import setuptools

from pylibvirt import __version__

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name='pylibvirt',
    version=__version__,
    description='Python package to orchestrate libvirt API from yaml declaration file',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/Sevolith/Python-Libvirt/',
    download_url='https://gitlab.com/Sevolith/Python-Libvirt/',
    author='Sevolith',
    author_email='contactsevolith@gmail.com',
    maintainer='Sevolith',
    maintainer_email='contactsevolith@gmail.com',
    license='GPL-2.0-or-later',
    packages=setuptools.find_packages(exclude=("tests",)),
    setup_requires=['wheel'],
    install_requires=['rich==10.5.0',
                      'pyyaml==5.4.1',
                      'libvirt-python==7.5.0',
                      'click==8.0.1'
                      ],
    entry_points={
        'console_scripts': [
            'pylibvirt = pylibvirt.__main__:main'
        ]
    },
    keywords='Libvirt automation yaml',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
    ]
)
