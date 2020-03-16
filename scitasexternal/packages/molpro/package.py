# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Molpro(Package):
    """Molpro is an ab initio program for electronic structure calculations."""

    homepage = "http://www.molpro.net"
    url      = 'file://%s/molpro-2019.2.tar.gz' % os.getcwd()

    version('2019.2', sha256='168fb70b219166af5e463be4d1a459d6f3f9991cde5774b0a3c84d2a13f9cfd7')
    version('2015.1', sha256='a51df73acd54911fcc2d468ffa66676fb83117bb4e463eefe22dcaba4645c477')

    variant('mpi', default=True, description='Build with MPI support')

    depends_on('blas')
    depends_on('lapack')
    depends_on('python@:3')

    depends_on('mpi', when='+mpi')
    depends_on('eigen', when='@2019:')

    # For a successful installation of Molpro either the environment variable
    # $MOLPRO_KEY or the file $HOME/.molpro/token has to exist. The content
    # of those is not checked during the installation, so anything will work.
    # However, if none of those exist, the installation hangs (it tries to
    # contact their server and it asks for user name and password). During
    # runtime a valid key is needed (in the file lib/.token).

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix]
        if '^intel-mkl' in spec:
            options.append("--with-blas-path=%s/lib/intel64" %
                           spec['blas'].prefix)
        elif '^openblas' in spec:
            options.append("--with-blas=%s" % spec['blas'].libs)
        # Leaving open the possibility of using -lblas
        else:
            options.append("--with-blas-path=%s" % spec['blas'].prefix.lib)
        if '+mpi' in spec:
            options.append('FC=%s' % spec['mpi'].mpifc)
            options.append('CXX=%s' % spec['mpi'].mpicxx)
            if self.version < Version('2019'):
                if '%intel' in spec:
                    options.append('--enable-mpp=%s/intel64/include' %
                                   spec['mpi'].prefix)
                elif '%gcc':
                    options.append('--enable-mpp=%s' %
                                   spec['mpi'].prefix.include)
                    options.append('F90FLAGS=-ffree-line-length-none')
            else:
                options.append('--without-ga')
        configure(*options)

        # Molpro wants to use a variation of mpirun during the installation.
        # We need to change the LAUNCHER in CONFIG to something not MPI
        # dependent to avoid problems with Slurm.
        filter_file(r'^LAUNCHER=.*', 'LAUNCHER=%x', 'CONFIG')
        make()

        # Before the installation we change the launcher to srun (%x is the
        # Molpro executable itself) to conform to our cluster.
        filter_file(r'^LAUNCHER=.*', 'LAUNCHER=srun %x', 'CONFIG')

        make('install')

    def setup_environment(self, spack_env, run_env):
        if self.version < Version('2019'):
            dir_base_name='molprop'
        else:
            dir_base_name='molpro'
        directory='{0}_{1}_linux_x86_64_i8'.format(dir_base_name,
                                                   self.version.up_to(2).underscored)
        run_env.prepend_path('PATH', join_path(self.prefix,
                             directory, 'bin'))
