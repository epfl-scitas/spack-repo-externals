# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Ams(Package):
    """AMS is a DFT software for modelling chemistry."""

    homepage = "http://www.scm.com"
    url      = "file://fake_url.tar.gz"
    only_binary = True
    licensed = True

    version('2022.103')
    depends_on('mpi')

    def install(self, spec, prefix):
        pass

    def setup_run_environment(self, run_env):
        ams_base = '/ssoft/spack/external/ams/ams2022.103'

        run_env.set('AMSBIN', join_path(ams_base, 'bin'))
        run_env.set('AMSHOME', ams_base)
        run_env.set('AMSRESOURCES', join_path(ams_base, 'atomicdata'))

        run_env.set('SCMLICENSE', join_path(ams_base, 'license.txt'))
        run_env.set('SCM_TMPDIR', '/tmp')
        run_env.set('SCM_USE_LOCAL_IMPI', '1')

        run_env.prepend_path('PATH', join_path(ams_base, 'bin'))
