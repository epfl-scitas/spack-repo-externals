# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Crystal17(Package):
    """Crystal is a code for solid state chemistry and physics."""

    homepage = "http://www.crystal.unito.it/"
    url      = "file://%s/crystal17-1.0.2.tar.bz2" % os.getcwd()

    # This is not the original file coming from Crystal. This file contains
    # part of utils17.zip which are scripts used to run Crystal.
    version('1.0.2', '0ee57f63d400552c46c2dbf1092670d69458c98e6399fc29841ae84cd25c77ac')

    patch('Xmakes-Linux-intel-inc-1.0.2.patch')

    # According to:
    # http://www.theochem.unito.it/crystal_tuto/mssc2013_cd/tutorials/tuto_HPC/tuto_hpc.html
    # Pcrystal only scales to 10s of cores and for large systems
    # one should use MPPcrystal
    variant('pcrystal', default=True,
            description='Builds replicated data binary (Pcrystal)')
    variant('mppcrystal', default=True,
            description='Builds distributed data binary (MPPcrystal)')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+pcrystal')
    depends_on('mpi', when='+mppcrystal')
    # Currently only builds with Intel
    conflicts('%gcc')

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
            install_tree('utils17_mpi', 'bin')
        if spec.satisfies('+mppcrystal'):
            make('MPP')
            install_tree('utils17_mpp', 'bin')

        install_tree('bin', spec.prefix.bin)

    def setup_run_environment(self, run_env):
        run_env.set('CRY17_ROOT', self.prefix)
        run_env.set('CRY17_EXEDIR', self.prefix.bin)
        run_env.set('CRY17_UTILS', self.prefix.bin)
