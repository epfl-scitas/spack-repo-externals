# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install gurobi
#
# You can edit this file again by typing:
#
#     spack edit gurobi
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Gurobi(Package):
    """Gurobi is the most powerful mathematical optimization solver out there. And our team of PhDs is making it better every day. """
    homepage = "https://www.gurobi.com"
    url      = "https://packages.gurobi.com/8.1/gurobi8.1.1_linux64.tar.gz"

    licensed = True
    only_binary = True

    version('8.1.1', 'c030414603d88ad122246fe0e42a314fab428222d98e26768480f1f870b53484')
 
    def setup_environment(self, spack_env, run_env):
	run_env.set('GRB_LICENSE_FILE', join_path(self.prefix,'gurobi.lic'))
