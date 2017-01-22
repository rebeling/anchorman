try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="anchorman",
    version="0.5.0",
    author="matthias rebel",
    author_email="webmaster@rebeling.net",
    url="https://github.com/rebeling/anchorman",
    description=("Anchorman takes a list of terms and a text. It finds the "
                 "terms in this text and replaces them with another "
                 "representation."),
    license='Apache 2.0',
    keywords=["intext-links", "linking", "annotation", "tag", "hypertext"],
    packages=["anchorman"],
    # pytest_plugins=['pytest_profiling'],
    install_requires=["beautifulsoup4==4.4.1",
                      "html5lib==1.0b8",
                      "lxml",
                      "pytest-cov",
                      "pytest",
                      "pyyaml"],
    tests_require=['pytest==2.8.3', 'pytest-cov==2.2.0'],
    classifiers=('Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers',
                 'Natural Language :: English',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.7')
)
