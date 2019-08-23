##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os
import subprocess


class Molpro(Package):
    """Molpro is an ab initio program for electronic structure calculations."""

    homepage = "http://www.molpro.net"
    url      = "fake_url.tar.gz"

    version('2015.1',
            '13da76da1a150fb513a8b0a5da5ddce8',
            url='file://%s/.molpro/downloads/molpro-2016-12-05.tar.gz' %
            os.path.expanduser("~"))

    variant('mpi', default=True, description='Build with MPI support')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')

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
            # options.append("--with-blas='-L%s %s'" %
            #                (spec['blas'].prefix.lib,
            #                 spec['blas'].libs))
            options.append("--with-blas=%s" % spec['blas'].libs)
        # Leaving open the possibility of using -lblas
        else:
            options.append("--with-blas-path=%s" % spec['blas'].prefix.lib)
        if '+mpi' in spec:
            options.append('FC=%s' % spec['mpi'].mpifc)
            options.append('CXX=%s' % spec['mpi'].mpicxx)
            if '%intel' in spec:
                options.append('--enable-mpp=%s/intel64/include' %
                               spec['mpi'].prefix)
            else:
                options.append('F90FLAGS=-ffree-line-length-none')
                options.append('--enable-mpp=%s' % spec['mpi'].prefix.include)
        configure(*options)

        # DJ
        # Molpro wants to use mpirun_rsh during the installation.
        # We need to change the LAUNCHER in CONFIG to something not MPI
        # dependent to avoid problems with SLURM.
        subprocess.call(['sed', '-i',
                        's#^LAUNCHER=.*#LAUNCHER="%x"#',
                         'CONFIG'])

        make()
        # Before the installation we change the launcher to srun (%x is the
        # Molpro executable itself) to conform to our cluster.
        subprocess.call(['sed', '-i',
                         's#^LAUNCHER=.*#LAUNCHER=srun %x#',
                         'CONFIG'])

        make('install')

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', join_path(self.prefix,
                             'molprop_2015_1_linux_x86_64_i8', 'bin'))
