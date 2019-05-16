from spack import *


class Ansys(Package):
    """Ansys Fluent - To use this software you need to be a member of the ansys-users group

    Please see http://ansys.epfl.ch for further information
    """

    homepage = "http://www.ansys.com"
    url = 'fakeurl.tar.gz'
    licensed = True
    only_binary = True

    version('19.2')
    version('17.1')

    def install(self, spec, prefix):
        pass

    def setup_environment(self, spack_env, run_env):
        version = self.spec.version
        ansys_prefix = '/ssoft/spack/external/ansys/{0}/v{1}'.format(
            version.up_to(2).dotted(),
            version.up_to(2).joined())
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'ansys/bin')
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'CFD-Pos/bin')
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'CFX/bin')
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'Icepak/bin')
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'TurboGrid/bin')
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'autodyn/bin')
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'fluent/bin')
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'polyflow/bin')
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'tgrid/bin')  
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'Framework/bin/Linux64')  # noqa: E501
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'icemcfd/linux64_amd/bin')  # noqa: E501

        run_env.prepend_path('LD_LIBRARY_PATH', join_path(ansys_prefix, 'Framework/bin/Linux64')  # noqa: E501
        run_env.prepend_path('LD_LIBRARY_PATH', join_path(ansys_prefix, 'polyflow/polyflow17.1.0/lnamd64/libs')  # noqa: E501
        run_env.prepend_path('LD_LIBRARY_PATH', join_path(ansys_prefix, 'Framework/bin/Linux64/Mesa')  # noqa: E501
