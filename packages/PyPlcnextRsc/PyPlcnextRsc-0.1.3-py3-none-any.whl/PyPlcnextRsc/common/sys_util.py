import sys

SPHINX_AUTODOC_RUNNING = "sphinx.ext.autodoc" in sys.modules


def PYVER_IS_NEW_THAN(major, minor, micro):
    inf = sys.version_info
    if major > inf.major:
        return False
    elif major == inf.major and minor > inf.minor:
        return False
    elif minor == inf.minor and micro > inf.micro:
        return False
    else:
        return True
