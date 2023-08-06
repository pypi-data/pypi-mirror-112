from pbr.version import VersionInfo

all = ('__version__')

# Check the PBR version module docs for other options than release_string()
__version__ = VersionInfo('nastja').release_string()
