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

import shutil

from spack import *


class Amber(Package):
    """A suite of programs that allow users to carry out molecular dynamics
    simulations, particularly on biomolecules.
    """

    homepage = 'http://ambermd.org'
    url = 'file:///fake/path/to/amber-16.tgz'

    version('18', 'ae5438d3f1e2d3379d5664c34193ae48')
    version('16', '652e24512146e966a0a50335572ebd66')

    # FIXME: separate ambertools and amber

    variant('mpi', default=True, description='Enables MPI support')
    variant('openmp', default=False, description='Enables OpenMP support')
    variant('cuda', default=False, description='Enables CUDA support')
    variant('X', default=False, description='Enables X11 support')
    # As of September 2018 AmberTools packmol_memgen is the only
    # boost-dependent part. However, AmberTools fails to compile if boost
    # support is included, due to a bug. By putting packmol as a variant,
    # AmberTools can be compiled in spite of this specific issue.
    variant('packmol', default=False,
            description='Compiles the optional packmol_memgen')

    depends_on('boost', when='+packmol')
    depends_on('cuda', when='+cuda')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')

    depends_on('netcdf~mpi', when='~mpi')
    depends_on('netcdf-fortran ^netcdf~mpi', when='~mpi')

    depends_on('netcdf+mpi', when='+mpi')
    depends_on('netcdf-fortran ^netcdf+mpi', when='+mpi')

    depends_on('python')
    depends_on('py-numpy')
    depends_on('py-scipy')
    depends_on('py-matplotlib', when='+X')

    # There is probably a bug in the Makefile and in some cases the parallel
    # build of Sander fails. Putting this here until the problem is fixed.
    parallel = False

    @property
    def wdir(self):
        return join_path(self.prefix, 'amber{0}'.format(self.spec.version))

    @property
    def configure_file(self):
        return join_path(self.stage.source_path, 'configure')

    @property
    def ambertools_configure_file(self):
        return join_path(
            self.stage.source_path, 'AmberTools', 'src', 'configure2'
        )

    def setup_environment(self, spack_env, run_env):

        spack_env.set('AMBERHOME', self.wdir)

        run_env.prepend_path('PATH', join_path(self.wdir, 'bin'))

        run_env.set('AMBERHOME', self.wdir)

        if '%intel' in self.spec:
            spack_env.set('MKL_HOME', self.spec['mkl'].prefix)

        if '+cuda' in self.spec:
            spack_env.set('CUDA_HOME', self.spec['cuda'].prefix)

    def patch(self):
        # Remove interaction from configure
        filter_file('read answer', 'answer="yes"', self.configure_file)

        # Add flags that are necessary to compile and link against an
        # external NETCDF to the configure2 file
        filter_file(
            "^ldflags=''",
            "ldflags='-L{0} '".format(self.spec['netcdf-fortran'].prefix.lib),
            self.ambertools_configure_file
        )

        filter_file(
            'netcdf=$netcdf_dir"/include/netcdf.mod"',
            "netcdf='{0}/netcdf.mod '".format(
                self.spec['netcdf-fortran'].prefix.include
            ),
            self.ambertools_configure_file,
            string=True
        )

    def install(self, spec, prefix):

        # Move source path into prefix
        shutil.copytree(
            self.stage.source_path,
            join_path(self.prefix, 'amber{0}'.format(spec.version))
        )

        with working_dir(self.wdir):
            # Amber needs to be built serially first and then
            # MPI eventually
            configure_args = [
                '--with-python {0}'.format(
                    join_path(spec['python'].prefix, 'bin', 'python')
                ),
                '--with-netcdf {0}'.format(
                    join_path(spec['netcdf'].prefix)
                )
            ]

            if '+X' not in spec:
                configure_args.append('-noX11')

            if '+openmp' in spec:
                configure_args.append('-openmp')

            # Maps C compiler to the corresponding option
            compiler_opts = {
                'gcc': 'gnu',
                'intel': 'intel',
                'clang': 'clang'
            }
            serial_args = configure_args[:]
            serial_args.append(compiler_opts[self.compiler.name])

            configure(*serial_args)

            # TODO: Here Amber documentation advise to source a shell script
            # TODO: that sets AMBERHOME. Add it as it could have side effects?
            make('install')

            if '+mpi' in spec:
                configure_args.append('-mpi')
                if 'intel-mpi' in spec:
                    configure_args.append('-intelmpi')
                parallel_args = configure_args[:]
                parallel_args.append(compiler_opts[self.compiler.name])

                configure(*parallel_args)
                make('install')

            if '+cuda' in spec:
                configure_args.append('-cuda')
                cuda_args = configure_args[:]
                cuda_args.append(compiler_opts[self.compiler.name])
                filter_file(
                    r'(nvccflags=")(.*)(")',
                    r'\1\2 $sm35flags \3',
                    'AmberTools/src/configure2'
                )
                configure(*cuda_args)
                make('install')
