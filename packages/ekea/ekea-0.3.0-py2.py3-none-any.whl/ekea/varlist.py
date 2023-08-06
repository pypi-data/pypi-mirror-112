import os, subprocess, json, shutil
from microapp import App, appdict
from ekea.utils import xmlquery

here = os.path.dirname(os.path.abspath(__file__))

class VariableList(App):
    _name_ = "varlist"
    _version_ = "0.1.0"

    def __init__(self, mgr):

        self.add_argument("casedir", metavar="casedir", help="E3SM case directory")
        self.add_argument("callsitefile", metavar="callsitefile", help="Ekea callsite Fortran source file")
        self.add_argument("-o", "--outdir", type=str, help="output directory")

        self.register_forward("data", help="json object")

    def perform(self, args):

        casedir = os.path.abspath(os.path.realpath(args.casedir["_"]))
        callsitefile = os.path.abspath(os.path.realpath(args.callsitefile["_"]))
        csdir, csfile = os.path.split(callsitefile)
        csname, csext = os.path.splitext(csfile)
        outdir = os.path.abspath(os.path.realpath(args.outdir["_"])) if args.outdir else os.getcwd()

        cleancmd = "cd %s; ./case.build --clean-all" % casedir
        buildcmd = "cd %s; ./case.build" % casedir
        runcmd = "cd %s; ./case.submit" % casedir

        # TODO: move this batch support to common area

        batch = xmlquery(casedir, "BATCH_SYSTEM", "--value")
        if batch == "lsf":
            runcmd += " --batch-args='-K'"

        elif "slurm" in batch:
            runcmd += " --batch-args='-W'"

        elif batch == "pbs": # SGE PBS
            runcmd += " --batch-args='-sync yes'"
            #runcmd += " --batch-args='-Wblock=true'" # PBS

        elif batch == "moab":
            runcmd += " --batch-args='-K'"

        else:
            raise Exception("Unknown batch system: %s" % batch)
 
        compjson = os.path.join(outdir, "compile.json")
        outfile = os.path.join(outdir, "model.json")
        srcbackup = os.path.join(outdir, "backup", "src")

        # get mpi and git info here(branch, commit, ...)
        srcroot = os.path.abspath(os.path.realpath(xmlquery(casedir, "SRCROOT", "--value")))
        reldir = os.path.relpath(csdir, start=os.path.join(srcroot, "components", "mpas-source", "src"))

        callsitefile2 = os.path.join(casedir, "bld", "cmake-bld", reldir, "%s.f90" % csname)

        # get mpi: mpilib from xmlread , env ldlibrary path with the mpilib
        mpidir = os.environ["MPI_ROOT"]
        excludefile = os.path.join(here, "exclude_e3sm_varlist.ini")

        blddir = xmlquery(casedir, "OBJROOT", "--value")
        if not os.path.isfile(compjson) and os.path.isdir(blddir):
            shutil.rmtree(blddir)

        cmd = " -- buildscan '%s' --savejson '%s' --reuse '%s' --backupdir '%s'" % (
                buildcmd, compjson, compjson, srcbackup)
        ret, fwds = self.manager.run_command(cmd)

        # save compjson with case directory map
        # handle mpas converted file for callsitefile2
        # TODO: replace ekea contaminated file with original files
        # TODO: recover removed e3sm converted files in cmake-bld, ... folders

        with open(compjson) as f:
            jcomp = json.load(f)

            for srcpath, compdata in jcomp.items():
                srcbackup = compdata["srcbackup"]

                if not srcbackup:
                    continue

                if not os.path.isfile(srcpath) and srcbackup[0] and os.path.isfile(srcbackup[0]):
                    orgdir = os.path.dirname(srcpath)

                    if not os.path.isdir(orgdir):
                        os.makedirs(orgdir)

                    shutil.copy(srcbackup[0], srcpath)

                for incsrc, incbackup in srcbackup[1:]:
                    if not os.path.isfile(incsrc) and incbackup and os.path.isfile(incbackup):
                        orgdir = os.path.dirname(incsrc)

                        if not os.path.isdir(orgdir):
                            os.makedirs(orgdir)

                        shutil.copy(incbackup, incsrc)
                
        # TODO: actually scan source files if they should be recovered

        #statedir = os.path.join(outdir, "state")
        #etimedir = os.path.join(outdir, "etime")

        #if os.path.isdir(statedir) and os.path.isfile(os.path.join(statedir, "Makefile")):
        #    stdout = subprocess.check_output("make recover", cwd=statedir, shell=True)

        #elif os.path.isdir(etimedir) and os.path.isfile(os.path.join(etimedir, "Makefile")):
        #    stdout = subprocess.check_output("make recover", cwd=etimedir, shell=True)

        #cmd = " -- resolve --compile-info '@data' '%s'" % callsitefile

        rescmd = (" -- resolve --mpi header='%s/include/mpif.h',build_resolver=true --openmp enable"
                 " --compile-info '%s' --exclude-ini '%s' '%s'" % (
                mpidir, compjson, excludefile, callsitefile2))
        #ret, fwds = prj.run_command(cmd)
        #assert ret == 0

        cmd = rescmd + " -- vargen '@analysis' --outdir '%s'" % outdir
        ret, fwds = self.manager.run_command(cmd)
