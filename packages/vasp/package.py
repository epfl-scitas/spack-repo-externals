# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Vasp(MakefilePackage):
    """
    The Vienna Ab initio Simulation Package (VASP)
    is a computer program for atomic scale materials modelling,
    e.g. electronic structure calculations
    and quantum-mechanical molecular dynamics, from first principles.
    """

    homepage = "https://vasp.at"
    url = "file://{0}/vasp.5.4.4.pl2.tgz".format(os.getcwd())
    manual_download = True

    version("6.4.1", sha256="4747e7403ecd114c56ada213cf8745e177e874aa4553897dcc21e9d43e67140c")
    version("6.3.2", sha256="f7595221b0f9236a324ea8afe170637a578cdd5a837cc7679e7f7812f6edf25a")
    version("6.2.1", sha256="d25e2f477d83cb20fce6a2a56dcee5dccf86d045dd7f76d3ae19af8343156a13")
    version("6.1.1", sha256="e37a4dfad09d3ad0410833bcd55af6b599179a085299026992c2d8e319bf6927")
    version("5.4.4.pl2", sha256="98f75fd75399a23d76d060a6155f4416b340a1704f256a00146f89024035bc8e")
    version("5.4.4", sha256="5bd2449462386f01e575f9adf629c08cb03a13142806ffb6a71309ca4431cfb3")

    resource(
        name="vaspsol",
        git="https://github.com/henniggroup/VASPsol.git",
        tag="V1.0",
        when="+vaspsol",
    )

    variant("openmp", default=False, description="Enable openmp build")
    variant("shmem", default=True, description="Enable shared memory segments")
    variant("hdf5", default=False, description="Enables build with HDF5")
    variant("scalapack", default=False, description="Enables build with SCALAPACK")
    variant("cuda", default=False, description="Enables running on Nvidia GPUs")

    variant(
        "vaspsol",
        default=False,
        description="Enable VASPsol implicit solvation model\n"
        "https://github.com/henniggroup/VASPsol",
    )

    depends_on("rsync", type="build")
    depends_on("blas")
    depends_on("lapack")
    depends_on("fftw-api")
    depends_on("mpi", type=("build", "link", "run"))
    depends_on("scalapack", when="+scalapack")
    depends_on("cuda", when="+cuda")
    depends_on("qd", when="%nvhpc")
    depends_on("hdf5", when="+hdf5")

    conflicts(
        "%gcc@:8", msg="GFortran before 9.x does not support all features needed to build VASP"
    )
    conflicts("+vaspsol", when="+cuda", msg="+vaspsol only available for CPU")
    conflicts("+openmp", when="@:6.1", msg="OpenMP support was added on 6.2")
    conflicts("+cuda", when="@6.3:", msg="Previous CUDA support ended with 6.2. Use %nvhpc instead")
    conflicts("+hdf5", when="@:6.1", msg="HDF5 support was added on 6.2")

    parallel = False

    def edit(self, spec, prefix):

        # Names of makefile.include files changed on 6.3
        if spec.satisfies("@6.3:"):
            base_name = 'makefile.include.'
        else:
            base_name = 'makefile.include.linux_'

        # This whole section is a bit of a mess, but the naming is not very standard
        # especially when it comes to OpenMP files
        if spec.satisfies("%gcc"):
            if spec.satisfies("@6.3:"):
                if spec.satisfies("^mkl"):
                    if spec.satisfies("+openmp"):
                        make_include = join_path("arch", base_name + "gnu_ompi_mkl_omp")
                    else:
                        make_include = join_path("arch", base_name + "gnu_ompi_mkl_omp")
                        filter_file(' -fopenmp', '', make_include)
                        filter_file('-lmkl_gnu_thread', '-lmkl_sequential', make_include)
                        filter_file('^LLIBS_MKL.*SCALAPACK_ROOT.*', '#LLIBS_MKL', make_include)
                    # if spec.satisfies('+scalapack'):
                    #     filter_file("^LLIBS_MKL.*", "LLIBS_MKL = {0} {1}".format(
                    #                 spec["scalapack"].libs.ld_flags,
                    #                 spec["blas"].libs.ld_flags), make_include)
                    # else:
                    #     filter_file("^LLIBS_MKL.*", "LLIBS_MKL = {}".format(
                    #                 spec["blas"].libs.ld_flags), make_include)
                elif spec.satisfies("+openmp"):
                    make_include = join_path("arch", base_name + "gnu_omp")
                else:
                    make_include = join_path("arch", base_name + "gnu")
                if spec.satisfies("gcc@:9"):
                    filter_file("^FFLAGS.*fallow-argument-mismatch",
                                "#FFLAGS += -fallow-argument-mismatch", make_include)
            elif spec.satisfies("+openmp"):
                make_include = join_path("arch", base_name + "gnu_omp")
            else:
                make_include = join_path("arch", base_name + "gnu")
        elif spec.satisfies("%intel"):
            if spec.satisfies("+openmp"):
                make_include = join_path("arch", base_name + "intel_omp")
            else:
                make_include = join_path("arch", base_name + "intel")

            # A workaround to get fpp
            filter_file('fpp', self.compiler.fc, make_include)
            filter_file('ifort -f_com', 'fpp -f_com', make_include)
        elif spec.satisfies("%nvhpc"):
            if spec.satisfies("@6.3:"):
                if spec.satisfies("+openmp"):
                    make_include = join_path("arch", base_name + "nvhpc_omp_acc")
                else:
                    make_include = join_path("arch", base_name + "nvhpc_acc")
                filter_file("nvfortran", spack_fc, make_include)
            else:
                make_include = join_path("arch", base_name + "nv_acc")
        elif spec.satisfies("%aocc"):
            if spec.satisfies("@6.3:"):
                if spec.satisfies("+openmp"):
                    make_include = join_path("arch", base_name + "aocc_ompi_aocl_omp")
                else:
                    make_include = join_path("arch", base_name + "aocc_ompi_aocl")
            else:
                if spec.satisfies("+openmp"):
                    copy(
                        join_path("arch", base_name + "gnu_omp"),
                        join_path("arch", base_name + "aocc_omp"),
                    )
                    make_include = join_path("arch", base_name + "aocc_omp")
                else:
                    copy(
                        join_path("arch", base_name + "gnu"),
                        join_path("arch", base_name + "aocc"),
                    )
                    make_include = join_path("arch", base_name + "aocc")
                filter_file("gcc", "{0} {1}".format(spack_cc, "-Mfree"), make_include, string=True)
                filter_file("g++", spack_cxx, make_include, string=True)
                filter_file("^CFLAGS_LIB[ ]{0,}=.*$", "CFLAGS_LIB = -O3", make_include)
                filter_file("^FFLAGS_LIB[ ]{0,}=.*$", "FFLAGS_LIB = -O2", make_include)
                filter_file("^OFLAG[ ]{0,}=.*$", "OFLAG = -O3", make_include)
                filter_file(
                    "^FC[ ]{0,}=.*$", "FC = {0}".format(spec["mpi"].mpifc), make_include, string=True
                )
                filter_file(
                    "^FCL[ ]{0,}=.*$", "FCL = {0}".format(spec["mpi"].mpifc), make_include, string=True
                )
        else:
            if spec.satisfies("+openmp"):
                make_include = join_path(
                    "arch", base_name + "{0}_omp".format(spec.compiler.name)
                )
            else:
                make_include = join_path("arch", base_name + spec.compiler.name)

        # Setting compilers to spack-based ones
        filter_file("^FC\s+= \S+", "FC = {0}".format(spec['mpi'].mpifc), make_include)
        filter_file("^FCL\s+= \S+", "FCL = {0}".format(spec['mpi'].mpifc), make_include)
        filter_file("^FC_LIB\s+= \S+", "FC_LIB = {0}".format(spack_fc), make_include)
        filter_file("^CC_LIB\s+= \S+", "CC_LIB = {0}".format(spack_cc), make_include)
        filter_file("^CXX_PARS\s+= \S+", "CXX_PARS = {0}".format(spack_cxx), make_include)
 
        if spec.satisfies("+hdf5"):
            if spec.satisfies("@6.3:"):
                filter_file("^#LLIBS\s+\+= -L\$\(HDF5_ROOT\)", "LLIBS += -L$(HDF5_ROOT)", make_include)
                filter_file("^#INCS\s+\+= -I\$\(HDF5_ROOT\)", "INCS += -I$(HDF5_ROOT)", make_include)
            # VASP 6.2 supports HDF5, but the makefile.includes proposed do not include it
            # Avoiding a patch to make it as generic as possible
            else:
                filter_file("^LLIBS\s+=", "LLIBS = -L{} ".format(spec["hdf5"].libs.ld_flags), make_include)
                if spec.satisfies("^mkl"):
                    filter_file("^INCS\s+=-I\$\(MKL", "INCS = -I$(HDF5_ROOT)/include -I$(MKL", make_include)
                else:
                    filter_file("^INCS\s+= -I\$\(FFTW", "INCS = -I$(HDF5_ROOT)/include -I$(FFTW", make_include)

        if spec.satisfies("+shmem"):
            # From here:
            # https://www.vasp.at/wiki/index.php/Shared_memory
            filter_file("^OBJECTS_LIB = linpack_double.o", "OBJECTS_LIB = linpack_double.o getshmem.o", make_include)

        # Recommended addition for non-MKL OpenMP builds
        if spec.satisfies("@6.2:") and spec.satisfies('+openmp') and not spec.satisfies('^mkl'):
            filter_file("^#CPP_OPTIONS\+= -Dsysv", "CPP_OPTIONS+= -Dsysv", make_include)
            filter_file("^#FCL\s+\+= fftlib.o", "FCL += fftlib.o", make_include)
            filter_file("^#CXX_FFTLIB", "CXX_FFTLIB", make_include)
            filter_file("^#INCS_FFTLIB", "INCS_FFTLIB", make_include)
            filter_file("^#LIBS\s+\+= fftlib", "LIBS += fftlib", make_include)
            filter_file("^#LLIBS\s+\+= -ldl", "LLIBS += -ldl", make_include)

        # This bunch of 'filter_file()' is to make these options settable
        # as environment variables
        filter_file("^CPP_OPTIONS[ ]{0,}=[ ]{0,}", "CPP_OPTIONS ?= ", make_include)
        filter_file("^FFLAGS[ ]{0,}=[ ]{0,}", "FFLAGS ?= ", make_include)

        filter_file("^LIBDIR[ ]{0,}=.*$", "", make_include)
        filter_file("^BLAS[ ]{0,}=.*$", "BLAS ?=", make_include)
        filter_file("^LAPACK[ ]{0,}=.*$", "LAPACK ?=", make_include)
        filter_file("^FFTW[ ]{0,}?=.*$", "FFTW ?=", make_include)
        filter_file("^MPI_INC[ ]{0,}=.*$", "MPI_INC ?=", make_include)
        filter_file("-DscaLAPACK.*$\n", "", make_include)
        filter_file("^SCALAPACK[ ]{0,}=.*$", "SCALAPACK ?=", make_include)
        filter_file("^QD[ ]{0,}=.*$", "QD ?=", make_include)

        if spec.satisfies("+cuda"):
            filter_file("^OBJECTS_GPU[ ]{0,}=.*$", "OBJECTS_GPU ?=", make_include)
            filter_file("^CPP_GPU[ ]{0,}=.*$", "CPP_GPU ?=", make_include)
            filter_file("^CFLAGS[ ]{0,}=.*$", "CFLAGS ?=", make_include)
            filter_file("^CC\s+= \w+", "CC = {0}".format(spack_cc), make_include)
            filter_file("^CXX\s+= \w+", "CXX = {0}".format(spack_cc), make_include)

        if spec.satisfies("+vaspsol"):
            copy("VASPsol/src/solvation.F", "src/")

        os.rename(make_include, "makefile.include")

    def setup_build_environment(self, spack_env):
        spec = self.spec

        cpp_options = [
            "-DMPI -DMPI_BLOCK=8000",
            "-Duse_collective",
            "-DCACHE_SIZE=4000",
            "-Davoidalloc",
            "-Duse_bse_te",
            "-Dtbdyn",
        ]

        if spec.satisfies("+openmp"):
            cpp_options.append("-D_OPENMP")

        if spec.satisfies("+shmem"):
            cpp_options.append("-Duse_shmem")

        if spec.satisfies("%nvhpc"):
            if spec.satisfies("@6.3:"):
                cpp_options.extend('-DHOST=\\"LinuxNV\\"')
            else:
                cpp_options.extend('-DHOST=\\"LinuxPGI\\"')
            cpp_options.extend(["-Dqd_emulate", "-Dfock_dblbuf", "-D_OPENACC", "-DUSENCCL", "-DUSENCCLP2P"])
        elif spec.satisfies("%aocc"):
            cpp_options.extend(['-DHOST=\\"LinuxGNU\\"', "-Dfock_dblbuf"])
        elif spec.satisfies("%intel"):
            cpp_options.append('-DHOST=\\"LinuxIFC\\"')
        else:
            cpp_options.append('-DHOST=\\"LinuxGNU\\"')

        if spec.satisfies("@6:"):
            cpp_options.append("-Dvasp6")

        cflags = ["-fPIC", "-DADD_"]
        fflags = []
        if spec.satisfies("%gcc") or spec.satisfies("%intel"):
            fflags.append("-w")
        elif spec.satisfies("%nvhpc"):
            fflags.extend(["-Mbackslash", "-Mlarge_arrays"])
        elif spec.satisfies("%aocc"):
            fflags.extend(["-fno-fortran-main", "-Mbackslash", "-ffast-math"])

        spack_env.set("BLAS", spec["blas"].libs.ld_flags)
        spack_env.set("LAPACK", spec["lapack"].libs.ld_flags)

        if spec.satisfies("@6.3:"):
            spack_env.set("FFTW_ROOT", spec["fftw-api"].prefix)
        else:
            spack_env.set("FFTW", spec["fftw-api"].prefix)

        spack_env.set("MPI_INC", spec["mpi"].prefix.include)

        if spec.satisfies("%nvhpc"):
            spack_env.set("QD", spec["qd"].prefix)

        if spec.satisfies("+scalapack"):
            cpp_options.append("-DscaLAPACK")
            spack_env.set("SCALAPACK", spec["scalapack"].libs.ld_flags)

        if spec.satisfies("+cuda"):
            cpp_gpu = [
                "-DCUDA_GPU",
                "-DRPROMU_CPROJ_OVERLAP",
                "-DCUFFT_MIN=28",
                "-DUSE_PINNED_MEMORY",
            ]

            objects_gpu = [
                "fftmpiw.o",
                "fftmpi_map.o",
                "fft3dlib.o",
                "fftw3d_gpu.o",
                "fftmpiw_gpu.o",
            ]

            cflags.extend(["-DGPUSHMEM=300", "-DHAVE_CUBLAS"])

            spack_env.set("CUDA_ROOT", spec["cuda"].prefix)
            spack_env.set("CPP_GPU", " ".join(cpp_gpu))
            spack_env.set("OBJECTS_GPU", " ".join(objects_gpu))

        if spec.satisfies("+hdf5"):
            cpp_options.append("-DVASP_HDF5")
            spack_env.set("HDF5_ROOT", spec["hdf5"].prefix)

        if spec.satisfies("+vaspsol"):
            cpp_options.append("-Dsol_compat")

        if spec.satisfies("%gcc@10:"):
            fflags.append("-fallow-argument-mismatch")

        # Finally
        spack_env.set("CPP_OPTIONS", " ".join(cpp_options))
        spack_env.set("CFLAGS", " ".join(cflags))
        spack_env.set("FFLAGS", " ".join(fflags))

    def build(self, spec, prefix):
        if spec.satisfies("+cuda"):
            make("gpu", "gpu_ncl")
        else:
            make("std", "gam", "ncl")

    def install(self, spec, prefix):
        install_tree("bin/", prefix.bin)
