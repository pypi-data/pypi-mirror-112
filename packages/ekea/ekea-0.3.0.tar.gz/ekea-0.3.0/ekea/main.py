from fortlab import Fortlab

from ekea.mpasocn import MPASOcnKernel
from ekea.eam import EAMKernel
from ekea.timing import KernelTimeGenerator, KernelTimeViewer
from ekea.varlist import VariableList

class E3SMKea(Fortlab):

    _name_ = "ekea"
    _version_ = "0.3.0"
    _description_ = "E3SM Fortran Kernel Extraction and Analysis"
    _long_description_ = "E3SM Fortran Kernel Extraction and Analysis"
    _author_ = "Youngsung Kim"
    _author_email_ = "youngsung.kim.act2@gmail.com"
    _url_ = "https://github.com/grnydawn/ekea"
    _builtin_apps_ = [MPASOcnKernel, EAMKernel, KernelTimeGenerator,
                      KernelTimeViewer, VariableList]

    def __init__(self):
        pass
