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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install ansys
#
# You can edit this file again by typing:
#
#     spack edit ansys
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Ansys(Package):
    """
    Ansys Fluent - To use this software you need to be a member of the
    ansys-users group Please see http://ansys.epfl.ch for further information
    """

    homepage = "http://www.ansys.com"
    url = 'fakeurl.tar.gz'
    licensed = True
    only_binary = True

    version('2022R2')
    version('2022R1')
    version('2020R2')
    version('19.2')
    version('17.1')

    def install(self, spec, prefix):
        pass

    def setup_environment(self, spack_env, run_env):
        version_mapping = { '2020R2': '20.2',
                            '2022R1': '22.1',
                            '2022R2': '22.2'}
        version = self.spec.version

        if str(version) in version_mapping:
           version = Version(version_mapping[str(version)])
        version_dotted = version.up_to(2).dotted

        ansys_prefix = self.prefix

        run_env.prepend_path('PATH', join_path(ansys_prefix, 'ansys/bin'))
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'CFD-Post/bin'))
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'CFX/bin'))
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'Icepak/bin'))
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'TurboGrid/bin'))
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'autodyn/bin'))
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'fluent/bin'))
        run_env.prepend_path('PATH', join_path(ansys_prefix, 'polyflow/bin'))

        run_env.prepend_path(
            'PATH',
            join_path(ansys_prefix, 'RSM/Config/tools/linux'))

        if version == Version('17.1'):
            run_env.prepend_path('PATH', join_path(ansys_prefix, 'tgrid/bin'))

        run_env.prepend_path(
            'PATH',
            join_path(ansys_prefix, 'Framework/bin/Linux64'))
        run_env.prepend_path(
            'PATH',
            join_path(ansys_prefix, 'icemcfd/linux64_amd/bin'))

        if version < Version('20.2'):
            run_env.prepend_path(
                'LD_LIBRARY_PATH',
                join_path(ansys_prefix, 'Framework/bin/Linux64'))
            run_env.prepend_path(
                'LD_LIBRARY_PATH',
                join_path(
                    ansys_prefix,
                    'polyflow/polyflow{0}.0/lnamd64/libs'.format(version.up_to(2).dotted))) # noqa: E501
            run_env.prepend_path(
                'LD_LIBRARY_PATH',
                join_path(ansys_prefix, 'Framework/bin/Linux64/Mesa'))
