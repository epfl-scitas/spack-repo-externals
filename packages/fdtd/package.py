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


class Fdtd(Package):
    """3D/2D Maxwell's solver for nanophotonic devices."""

    homepage = "https://www.lumerical.com/products/fdtd/"
    url = "fakeurl.tar.gz"
    licensed = True
    only_binary = True

    version("2022-R1.1-2963")
    version("2021-R2.2-2806")
    version("2020-R2.4-2502")
    version("2020-R2-2387")
    version("8.24.2387")
    version("8.20.1703")
    version("8.19.1416-1")
    version("8.18.1365-1")
    version("8.12.527")
