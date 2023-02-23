# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Terachem(Package):
    """TeraChem is general purpose quantum chemistry software designed to
       run on NVIDIA GPUs."""

    homepage = "https://www.petachem.com"
    url      = "file://fake_url.tar.gz"
    only_binary = True

    version('1.96H-beta')

    def install(self, spec, prefix):
        pass

    def setup_run_environment(self, run_env):
        tera_base = '/ssoft/spack/external/terachem'
        tera_root = join_path(tera_base, str(self.spec.version), 'TeraChem')

        run_env.set('TeraChem', tera_root)
        run_env.set('NBOEXE', join_path(tera_root, 'bin', 'nbo6.i4.exe'))

        run_env.prepend_path('LD_LIBRARY_PATH', join_path(tera_root, 'lib'))
        run_env.prepend_path('PATH', join_path(tera_root, 'bin'))
