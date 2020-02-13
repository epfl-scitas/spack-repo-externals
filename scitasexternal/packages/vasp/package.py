# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

from spack import *


class Vasp(Package):
    """VASP is a plane wave electronic structure code."""

    homepage = "http://www.vasp.at"
    url      = "fake_url.tar.gz"
    licensed = True

    version('5.4.4',
            sha256='5bd2449462386f01e575f9adf629c08cb03a13142806ffb6a71309ca4431cfb3',
            url='file://%s/vasp.5.4.4.tar.gz' % os.getcwd())

    variant('mpi', default=True, description='Build with MPI support')

    depends_on('blas')
    depends_on('lapack')
    # Our intel-mkl module is still not up to date and it does not include
    # provides('fftw'). With a newer version this depends on does not need
    # the when='%gcc')
    depends_on('fftw', when='%gcc')
    depends_on('mpi', when='+mpi')
    depends_on('scalapack', when='+mpi')

    parallel = False

    def install(self, spec, prefix):
        if '%intel' in spec:
            arch_file = join_path('arch', 'makefile.include.linux_intel')
            # Our spack recipe for intel-mkl breaks $MKLROOT. Otherwise we
            # woiuldn't need these two lines
            filter_file(r'\$\(MKLROOT\)', '%s' % os.environ["MKLROOT"],
                        arch_file)
            filter_file('mkl/compilers_and_libraries/linux/mkl', 'mkl',
                        arch_file)

        if '%gcc' in spec:
            arch_file = join_path('arch', 'makefile.include.linux_gnu')
            filter_file(r'mpif90', '%s' % spec['mpi'].mpifc, arch_file)
            filter_file(r'^BLAS\s*=.*', 'BLAS = -L%s -lopenblas'
                        % spec['blas'].prefix.lib, arch_file)
            filter_file(r'^LAPACK\s*=.*', 'LAPACK =', arch_file)
            filter_file(r'^SCALAPACK\s*=.*', 'SCALAPACK = -L%s -lscalapack'
                        % spec['scalapack'].prefix.lib, arch_file)
            filter_file(r'^FFTW\s*.=.*', 'FFTW = %s'
                        % spec['fftw'].prefix, arch_file)
            filter_file(r'^MPI_INC\s*.=.*', 'MPI_INC = %s'
                        % spec['mpi'].prefix.include, arch_file)

        shutil.copy(arch_file, 'makefile.include')
        make('all')
        shutil.copytree('bin', spec.prefix.bin)
