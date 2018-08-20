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


class Molden(Package):
    """MOLDEN is a processing program of molecular and electronic structure"""

    homepage = "http://www.cmbi.ru.nl/molden/"
    url      = "ftp://ftp.cmbi.ru.nl/pub/molgraph/molden/molden5.7.tar.gz"

    version('5.7', 'd4b32934c7a59108b1580c4d4fd8b17f')

    variant('gmolden', default=False,
            description='Additionally compile the OpenGL version of Molden')

    variant('ambfor', default=False,
            description='Additionally compile ambfor/ambmd')

    variant('surf', default=False,
            description='Additionally compile surf')

    depends_on('makedepend', type='build')

    def install(self, spec, prefix):
        make('molden')
        mkdirp(self.prefix.bin)

        install(
            os.path.join(self.stage.source_path, 'molden'),
            os.path.join(self.prefix.bin, 'molden')
        )

        if '+gmolden' in spec:
            make('gmolden')
            install(
                os.path.join(self.stage.source_path, 'gmolden'),
                os.path.join(self.prefix.bin, 'gmolden')
            )

        if '+ambfor' in spec:
            make('ambfor/ambfor')
            install(
                os.path.join(self.stage.source_path, 'ambfor', 'ambfor'),
                os.path.join(self.prefix.bin, 'ambfor')
            )
            install(
                os.path.join(self.stage.source_path, 'ambfor', 'ambmd'),
                os.path.join(self.prefix.bin, 'ambmd')
            )

        if '+surf' in spec:
            make('surf/surf')
            install(
                os.path.join(self.stage.source_path, 'surf', 'surf'),
                os.path.join(self.prefix.bin, 'surf')
            )
