from spack import *


class IntelAdvisor(Package):
    """
    Intel Advisor
    """
    homepage = "https://software.intel.com/content/www/us/en/develop/tools/advisor.html"
    url = 'fakeurl.tar.gz'
    licensed = True
    only_binary = True

    version('2019.5.0.602216')

    def setup_environment(self, spack_env, run_env):
        version = self.spec.version
        run_env.prepend_path('PKG_CONFIG_PATH',
                             join_path(self.prefix, 'include/pkgconfig/lib64'))
        run_env.prepend_path('PYTHONPATH', join_path(self.prefix, 'pythonapi'))
        run_env.prepend_path('PATH', join_path(self.prefix, 'bin64'))
        run_env.set_path('ADVISOR_{0}_DIR'.format(version.up_to(1)),
                         join_path(self.prefix, ''))

    def install(self, spec, prefix):
        pass
