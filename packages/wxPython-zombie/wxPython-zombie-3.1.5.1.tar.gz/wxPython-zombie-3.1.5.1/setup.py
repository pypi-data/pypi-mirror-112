import sys, os, re, glob, shutil
import pkg_info
from distutils.command.build import build
from setuptools              import setup, find_packages
try:
    from wheel.bdist_wheel   import bdist_wheel
except ImportError:
    cmd = '"{}" -m pip install wheel'.format(sys.executable)
    os.system(cmd)
    from wheel.bdist_wheel   import bdist_wheel


#-------------------------------------------------------------------------------

DESCRIPTION      = 'Cross platform GUI toolkit for Python, \'Zombie\' version'
MAINTAINER       = 'Stephan Zevenhuizen'
MAINTAINER_EMAIL = 'S.J.M.Zevenhuizen@uu.nl'
LICENSE          = 'wxWindows Library License '\
                   '(https://opensource.org/licenses/wxwindows.php)'
PLATFORMS        = 'win-amd64, linux-x86_64'
KEYWORDS         = 'GUI, wx, wxWindows, wxWidgets'

LONG_DESCRIPTION = open('README.txt', 'rb').read().decode().\
                   replace('\r\n', '\n').expandtabs(4)

CLASSIFIERS      = """\
Development Status :: 6 - Mature
Environment :: Win32 (MS Windows)
Environment :: X11 Applications :: GTK
Intended Audience :: Developers
License :: OSI Approved
Operating System :: Microsoft :: Windows :: Windows 10
Operating System :: POSIX :: Linux
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: Implementation :: CPython
Topic :: Software Development :: User Interfaces
"""

PACKAGES         = [pkg_info.TOP_LEVEL] + \
                   [pkg_info.TOP_LEVEL + '.' +
                    pkg for pkg in find_packages(pkg_info.TOP_LEVEL)]

ENTRY_POINTS     = {'console_scripts':
                    ['wxpython-demo = wx.demo:_main']}

#-------------------------------------------------------------------------------

class wx_build(build):

    def _get_soname(self, lib):
        output = os.popen('objdump -p %s' % lib).read()
        s = re.search('^\s+SONAME\s+(.+)$', output, re.M)
        return s.group(1)

    def _cleanup_symlinks(self, path):
        for lib in glob.glob(os.path.join(path, 'libwx*')):
            if os.path.islink(lib):
                soname = self._get_soname(lib)
                if soname == os.path.basename(lib):
                    real_file = os.path.join(path, os.readlink(lib))
                    os.unlink(lib)
                    os.rename(real_file, lib)
                else:
                    os.unlink(lib)

    def finalize_options(self):
        build.finalize_options(self)
        self.build_lib = self.build_platlib

    def run(self):
        cmd = '"{}" -u build.py build'.format(sys.executable)
        exit_status = os.system(cmd)
        if exit_status:
            print("Command '%s' failed with exit code %d." %
                  (cmd, exit_status))
            sys.exit(exit_status)
        shutil.copy('MANIFEST.bdist_wheel', 'MANIFEST.in')
        if os.name == 'posix' and not os.system('objdump -v'):
            self._cleanup_symlinks(pkg_info.TOP_LEVEL)
        build.run(self)


class wx_bdist_wheel(bdist_wheel):

    def _has_ext_modules(self):
        return True

    def finalize_options(self):
        self.distribution.has_ext_modules = self._has_ext_modules
        bdist_wheel.finalize_options(self)


CMDCLASS = {'build': wx_build, 'bdist_wheel': wx_bdist_wheel}

#-------------------------------------------------------------------------------

setup(name                 = pkg_info.NAME,
      version              = pkg_info.VERSION,
      description          = DESCRIPTION,
      long_description     = LONG_DESCRIPTION,
      maintainer           = MAINTAINER,
      maintainer_email     = MAINTAINER_EMAIL,
      license              = LICENSE,
      platforms            = PLATFORMS,
      classifiers          = [c for c in CLASSIFIERS.split('\n') if c],
      keywords             = KEYWORDS,
      install_requires     = pkg_info.INSTALL_REQUIRES,
      python_requires      = '>=3.5',
      zip_safe             = False,
      include_package_data = True,
      packages             = PACKAGES,
      ext_package          = pkg_info.TOP_LEVEL,
      entry_points         = ENTRY_POINTS,
      cmdclass             = CMDCLASS)
