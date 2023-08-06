import os, subprocess, json, shutil
from microapp import App, appdict
from ekea.utils import xmlquery

import numpy as np

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, MultiSelect, Select, Div
from bokeh.server.server import Server
from bokeh.layouts import column, row

here = os.path.dirname(os.path.abspath(__file__))

description = """
<h1>EKea Timing Plot</h1>
  
<p>
<h2>Interact with the widgets to query a subset of kernel timing to plot.</h2>
</p>
<br />
"""

class KernelTimeViewer(App):
    _name_ = "ktimeview"
    _version_ = "0.1.0"

    def __init__(self, mgr):

        self.add_argument("model", metavar="model", help="Timing model file")

    def modify_doc(self, doc):

        self.source = ColumnDataSource(data=dict(top=[], left=[], right=[]))

        self.kplot = figure()
        self.kplot.y_range.start = 0
        self.kplot.quad(top="top", bottom=0, left="left", right="right", source=self.source)

        desc = Div(text=description, sizing_mode="stretch_width")

        self.sel_procs = MultiSelect(title="Select MPI.OpenMP", options=self.procs, value=["All"])
        self.sel_plots = Select(title="Select Plot Type", options=self.plots, value=self.plots[0])
        self.sel_invokes = MultiSelect(title="Select invokes", options=self.invokes, value=["All"])

        controls = [self.sel_procs, self.sel_invokes, self.sel_plots]

        for control in controls:
            control.on_change("value", lambda attr, old, new: self.update())

        root = column(desc, row(self.sel_procs, column(self.sel_plots, self.kplot, self.sel_invokes)))

        self.update()

        doc.add_root(root)
        doc.title = "Kernel Timing"

    def perform(self, args):

        self.add_argument("model", metavar="model", help="Timing model file")

        with open(args.model["_"]) as f:
            self.jmodel = json.load(f)

        #self.source = ColumnDataSource(data=dict(top=[], left=[], right=[]))

        self.procs = ["All"]
        self.invokes = ["All"]
        self.plots = ["Elapsed Times", "Alignment"]

        self.labels = {
            "xlabel" : {
                self.plots[0] : "elapsed time (sec)",
                self.plots[1] : "Time deviation from the average (sec)"
            },

            "ylabel" : {
                self.plots[0] : "frequency",
                self.plots[1] : "frequency"
            }
        }

        for mpi, d1 in self.jmodel["etime"].items():
            if not mpi.isnumeric():
                continue

            for omp, d2 in d1.items():
                ylabel = mpi+"."+omp

                if ylabel not in self.procs:
                    self.procs.append(ylabel)

                for invoke in d2.keys():
                    if invoke not in self.invokes:
                        self.invokes.append(invoke)

        #src = pd.read_json("model.json")
        #summary = src.loc["_summary_"]
        #src = src.drop(labels=["_summary_"])

        server = Server({'/': self.modify_doc}, num_procs=4)
        server.start()
        server.io_loop.add_callback(server.show, "/")
        server.io_loop.start()

    def update(self):

        vals, x_name, y_name = self.select_timings()

        top, edges = np.histogram(vals, density=True, bins=min(100, len(vals)))

        self.kplot.xaxis.axis_label = x_name
        self.kplot.yaxis.axis_label = y_name
        self.kplot.title.text = ""

        self.source.data = dict(
            top= top,
            left= edges[:-1],
            right= edges[1:]
        )

    def select_timings(self):

        sel_plot = self.sel_plots.value
        sel_proc = self.sel_procs.value
        sel_invoke = self.sel_invokes.value

        min_etime = 10E10
        max_etime = 0.0
        resolution = None

        vals = []
        vallist = []
        valdict = {}

        for mpi, d1 in self.jmodel["etime"].items():
            if not mpi.isnumeric():
                continue

            for omp, d2 in d1.items():

                ylabel = mpi+"."+omp

                if "All" not in sel_proc and ylabel not in sel_proc:
                    continue

                for invoke in sorted(d2.keys(), key=int):

                    if "All" not in sel_invoke and invoke not in sel_invoke:
                        continue

                    interval = tuple(float(v) for v in d2[invoke])

                    if interval[0] < min_etime:
                        min_etime = interval[0]

                    if interval[1] < max_etime:
                        max_etime = interval[1]

                    if sel_plot == self.plots[0]:
                        vallist.append(abs(interval[0] - interval[1]))

                    elif sel_plot == self.plots[1]:
                        if invoke not in valdict:
                            valdict[invoke] = []

                        valdict[invoke].append(interval[0])

        if sel_plot == self.plots[0]:
            vals = vallist

        elif sel_plot == self.plots[1]:
            for invoke, stimes in valdict.items():
                valavg = sum(stimes) / float(len(stimes))
                vals.extend([s - valavg for s in stimes])

        x_name = self.labels["xlabel"][sel_plot]
        y_name = self.labels["ylabel"][sel_plot]

        return vals, x_name, y_name




class KernelTimeGenerator(App):
    _name_ = "ktimegen"
    _version_ = "0.1.0"

    def __init__(self, mgr):

        self.add_argument("casedir", metavar="casedir", help="E3SM case directory")
        self.add_argument("callsitefile", metavar="callsitefile", help="ekea callsite Fortran source file")
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
        excludefile = os.path.join(here, "exclude_e3sm_mpas.ini")

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

        statedir = os.path.join(outdir, "state")
        etimedir = os.path.join(outdir, "etime")

        if os.path.isdir(statedir) and os.path.isfile(os.path.join(statedir, "Makefile")):
            stdout = subprocess.check_output("make recover", cwd=statedir, shell=True)

        elif os.path.isdir(etimedir) and os.path.isfile(os.path.join(etimedir, "Makefile")):
            stdout = subprocess.check_output("make recover", cwd=etimedir, shell=True)

        #cmd = " -- resolve --compile-info '@data' '%s'" % callsitefile
        rescmd = (" -- resolve --mpi header='%s/include/mpif.h' --openmp enable"
                 " --compile-info '%s' --exclude-ini '%s' '%s'" % (
                mpidir, compjson, excludefile, callsitefile2))
        #ret, fwds = prj.run_command(cmd)
        #assert ret == 0

        # TODO wait??
        #cmd = rescmd + " -- runscan '@analysis' -s 'timing' --outdir '%s' --cleancmd '%s' --buildcmd '%s' --runcmd '%s' --output '%s'" % (
                    #outdir, cleancmd, buildcmd, runcmd, outfile)
        cmd = rescmd + " -- runscan '@analysis' -s 'timing' --outdir '%s' --buildcmd '%s' --runcmd '%s' --output '%s'" % (
                    outdir, buildcmd, runcmd, outfile)

        ret, fwds = self.manager.run_command(cmd)

        if os.path.isfile(outfile):
            with open(outfile) as f:
                mfile = json.load(f)
                if "etime" in mfile:
                    print("Kernel timing file is generated at '%s'." % outfile)

                else:
                    print("ERROR: wrong rkKernel timing file is generated at '%s'." % outfile)
        else: 
            print("No kernel timing file is generated.")
