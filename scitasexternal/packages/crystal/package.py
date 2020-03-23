# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Crystal(Package):
    """Crystal is a code for solid state chemistry and physics."""

    homepage = "http://www.crystal.unito.it/"
    url      = "file://%s/crystal17-1.0.2.tar.gz" % os.getcwd()

    version('1.0.2', '793e704f375298d0b660692de7f9976e8d58bc2cf2367f4132617641a86647e8')

    patch('Xmakes-Linux-intel-inc-1.0.2.patch', when='@1.0.2')

    # According to:
    # http://www.theochem.unito.it/crystal_tuto/mssc2013_cd/tutorials/tuto_HPC/tuto_hpc.html
    # Pcrystal only scales to 10s of cores and for large systems
    # one should use mppcrystal
    variant('pcrystal', default=True,
            description='Builds replicated data binary (Pcrystal)')
    variant('mppcrystal', default=True,
            description='Builds distributed data binary (MPPcrystal)')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+pcrystal')
    depends_on('mpi', when='+mppcrystal')

    def install(self, spec, prefix):
        os.chdir("build")
        filter_file(r'^ARCH =.*', 'ARCH = Linux-intel', 'Makefile')
        filter_file(r'^BINDIR .*', 'BINDIR = bin', 'Makefile')
        if spec.satisfies('~pcrystal') and spec.satisfies('~mppcrystal'):
            filter_file(r'^F90     =.*', 'F90     = %s' % self.compiler.fc,
                        'Xmakes/Linux-intel.inc')

        # Make serial version
        make()
        # and parallel versions
        if spec.satisfies('+pcrystal'):
            make('parallel')
        if spec.satisfies('+mppcrystal'):
            make('MPP')

        install_tree('bin', spec.prefix.bin)
