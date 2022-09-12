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
    """The Gurobi Optimizer was designed from the ground up to be the fastest,
    most powerful solver available for your LP, QP, QCP, and MIP (MILP, MIQP,
    and MIQCP) problems.
    Note: Gurobi is licensed software. You will need to create an account on
    the Gurobi homepage and download Gurobi Optimizer yourself. Spack will
    search your current directory for the download file. Alternatively, add
    this file to a mirror so that Spack can find it. For instructions on how to
    set up a mirror, see http://spack.readthedocs.io/en/latest/mirrors.html
    Please set the path to licence file with the following command (for bash)
    export GRB_LICENSE_FILE=/path/to/gurobi/license/. See section 4 in
    $GUROBI_HOME/docs/quickstart_linux.pdf for more details."""

    homepage = "http://www.gurobi.com/index"

    version('9.5.2', sha256='92e2d8972d3f0edec9c35eb5a7d5bd50390c5526a04aef50d771d2dd9d94a16a')
    version('9.1.0', sha256='92e2d8972d3f0edec9c35eb5a7d5bd50390c5526a04aef50d771d2dd9d94a16a')
    version('8.1.1', sha256='c030414603d88ad122246fe0e42a314fab428222d98e26768480f1f870b53484')
    version('7.5.2', sha256='d2e6e2eb591603d57e54827e906fe3d7e2e0e1a01f9155d33faf5a2a046d218e')

    # Licensing
    license_required = True
    license_files    = ['gurobi.lic']
    license_vars     = ['GRB_LICENSE_FILE']
    license_url      = 'http://www.gurobi.com/downloads/download-center'

    def url_for_version(self, version):
        url = "https://packages.gurobi.com/{0}/gurobi{1}_linux64.tar.gz"
        return url.format(version.up_to(2), version)

    def install(self, spec, prefix):
        install_tree('linux64', join_path(prefix, 'linux64'))

    @property
    def global_license_file(self):
        """Returns the path where a Spack-global license file should be stored.

        All Intel software shares the same license, so we store it in a
        common 'intel' directory."""
        return os.path.join(self.global_license_dir, 'gurobi', 'gurobi.lic')

    def setup_environment(self, spack_env, run_env):
        run_env.set('GRB_LICENSE_FILE', self.global_license_dir)
        run_env.set('GUROBI_HOME', join_path(prefix, 'linux64'))
        run_env.prepend_path('PATH', join_path(prefix, 'linux64', 'bin'))
        run_env.prepend_path('LD_LIBRARY_PATH', join_path(prefix, 'linux64',
                                                          'lib'))
