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
#
from spack import *


class Cfdplusplus(Package):
    """Metacomp's Computational Fluid Dynamics (CFD) software suite."""

    homepage = "http://www.metacomptech.com/index.php/features/icfd"
    url = 'fakeurl.tar.gz'
    licensed = True
    only_binary = True

    version('19.1')
    version('17.1')
    version('16.1')

    def install(self, spec, prefix):
        pass

    def setup_environment(self, spack_env, run_env):
        version =  self.spec.version.up_to(2).dotted
        prefix_version = version
        if self.spec.satisfies('@16.1'):
            prefix_version = '2016.05'
        
        prefix = '/ssoft/spack/external/CFD++/{0}'.format(prefix_version)
        mcfd_prefix = '{0}/mlib/mcfd.{1}'.format(prefix, version)

        run_env.set('CFDPLUSPLUS_ROOT', prefix)
        run_env.set('CFDPLUSPLUS_INCLUDE', prefix + '/include')
        run_env.set('CFDPLUSPLUS_LIBRARY', prefix + '/lib')
        run_env.set('CFDPLUSPLUS_PATH', mcfd_prefix + '/exec')
        run_env.prepend_path('LD_LIBRARY_PATH', prefix + '/lib')
        run_env.prepend_path('LD_LIBRARY_PATH', prefix + '/glib')
        run_env.set('METACOMP_LICENSE_FILE', prefix + '/Lics/Metacomp.lic')
        run_env.set('METACOMP_HOME', prefix + '')
        run_env.set('MCFD_HOME', mcfd_prefix)
        run_env.prepend_path('PATH', mcfd_prefix + '/exec')
        run_env.set('MCFD_TCLTK', mcfd_prefix + '/exec/gui_src')
        run_env.set('MCFD_HTML', mcfd_prefix + '/html')
        run_env.set('MCFD_VERSION', version)
        run_env.set('MCFD_PAR_LIC_MODE', '2')
        run_env.set('MCFD_MAXMEM', '512G')
        run_env.set('MCFD_PROCMEM', '32G')
        run_env.set('MCFD_GUIOPT1', 'MCFD_GUI_TNEQC')
        run_env.set('MCFD_TOGL', 'yes')
        run_env.set('TCL_LIBRARY', prefix + '/mlib/tcltk8/lib/tcl8.0')
        run_env.set('TK_LIBRARY', prefix + '/mlib/tcltk8/lib/tk8.0')
        run_env.set('MPATH', prefix + '/mbin')
