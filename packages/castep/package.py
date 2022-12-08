##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Castep(MakefilePackage):
    """
    CASTEP is a leading code for calculating the properties of materials from
    first principles.
    """

    homepage = "http://www.castep.org"
    url = "file://%s/CASTEP-21.11.tar.gz" % os.getcwd()
    licensed = True

    version('21.11', sha256='d909936a51dd3dff7a0847c2597175b05c8d0018d5afe416737499408914728f')

    depends_on('intel-mpi')
    depends_on('intel-mkl')
    depends_on('fftw-api@3')

    def setup_run_environment(self, run_env):
        run_env.prepend_path('PATH', self.prefix)

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make('ROOTDIR={}'.format(self.build_directory),
                 'FFT=mkl',
                 'FFTLIBDIR={}'.format(os.environ['MKLROOT']),
                 'MATHLIBS=mkl',
                 'MATHLIBDIR={}'.format(os.environ['MKLROOT']),
                 'ARCH=linux_x86_64_ifort',
                 'COMMS_ARCH=mpi'
                 )

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make('ROOTDIR={}'.format(self.build_directory),
                 'INSTALL_DIR={}'.format(prefix),
                 'install')
