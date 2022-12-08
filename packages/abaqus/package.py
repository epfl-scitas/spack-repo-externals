from spack import *

import spack.environment

class Abaqus(Package):
    """
    Abaqus at the EPFL is provided by the STI - http://sti.epfl.ch/it/page-37949-fr.html
    """

    homepage = "http://www.3ds.com/products-services/simulia/products/abaqus/latest-release"
    url = 'fakeurl.tar.gz'
    licensed = True
    only_binary = True


    version('6.14-1')

    def install(self, spec, prefix):
        pass


    def setup_run_environment(self, run_env):
        run_env.prepend_path('PATH', '/ssoft/spack/external/abaqus/6.14-1/code/bin')
