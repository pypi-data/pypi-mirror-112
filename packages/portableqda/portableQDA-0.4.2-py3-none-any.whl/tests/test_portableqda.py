"""
PortableQDA tests - main package
"""
from portableqda import __version__


def test_version():
    assert __version__ == '0.4.2'
    print(f"running PortableQDA { __version__}")
