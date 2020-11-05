# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Gurobi(Package):
    """Gurobi is the most powerful mathematical optimization solver out there.
       And our team of PhDs is making it better every day."""
    homepage = "https://www.gurobi.com"
    url      = "https://packages.gurobi.com/8.1/gurobi8.1.1_linux64.tar.gz"

    licensed = True
    only_binary = True

    version('8.1.1', 'c030414603d88ad122246fe0e42a314fab428222d98e26768480f1f870b53484')

    def url_for_version(self, version):
        url = "https://packages.gurobi.com/{0}/gurobi{1}_linux64.tar.gz"
        return url.format(version.up_to(2), version)

    def install(self, spec, prefix):
        install_tree("linux64", join_path(prefix, "linux64"))

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', join_path(prefix, 'linux64', 'bin'))
        run_env.set('GRB_LICENSE_FILE', join_path(prefix, 'linux64', 'gurobi.lic'))
