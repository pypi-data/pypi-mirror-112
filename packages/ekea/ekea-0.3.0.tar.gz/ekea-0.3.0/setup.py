"ekea setup module."

def main():

    from setuptools import setup, find_packages
    from ekea.main import E3SMKea as kea

    console_scripts = ["ekea=ekea.__main__:main"]
    install_requires = ["fortlab>=0.1.12"]

    setup(
        name=kea._name_,
        version=kea._version_,
        description=kea._description_,
        long_description=kea._long_description_,
        author=kea._author_,
        author_email=kea._author_email_,
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
        ],
        keywords="microapp fortlab ekea",
        packages=find_packages(exclude=["tests"]),
        include_package_data=True,
        install_requires=install_requires,
        entry_points={ "console_scripts": console_scripts,
            "microapp.projects": "ekea = ekea"},
        project_urls={
            "Bug Reports": "https://github.com/grnydawn/ekea/issues",
            "Source": "https://github.com/grnydawn/ekea",
        }
    )

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
