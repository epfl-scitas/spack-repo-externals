from spack import *


class Totalview(Package):
    """
    Totalview parallel debugger
    """

    homepage = "http://www.roguewave.com/products-services/totalview"
    url = 'file://fakeurl.tar.gz'
    licensed = True
    only_binary = True

    version('2020.3.11')
    version('2017.2.11')
    version('8.15.10-2')

    def install(self, spec, prefix):
        pass
