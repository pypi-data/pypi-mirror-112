import sys

cdef extern from "Python.h":
    ctypedef struct PyModuleDef:
        const char* m_name;

    void Py_INCREF(object)
    object PyModule_FromDefAndSpec(PyModuleDef *definition, object spec)
    int PyModule_ExecDef(object module, PyModuleDef* definition)

cdef extern from "series.h":
    object PyInit_03dbe33b62276c95dfcc6b35b29276d3c8f9eb00f1006964e2f49514eb537456()
cdef extern from "chunks/maker.h":
    object PyInit_f16fd407cfbfb2ad452d52d2b745d1660ec3173e6bc8a2b02919498dbc99c5a7()
cdef extern from "chunks/gzip.h":
    object PyInit_b7dee28f8f76409f72a74038ee6dd97f35b270b1992a243158290438c422783e()
cdef extern from "chunks/direct.h":
    object PyInit_7e8c3d09a1c13dc99e4a4ac22f2fec9087991da8316365c6b6b626504e3e829a()
cdef extern from "chunks/base.h":
    object PyInit_e4e05e6002b9e86a822bad12d8ff07494d560e0e6101b0d01364be04f15e053e()
cdef extern from "chunks/normal.h":
    object PyInit_336fb6b6488526368c1e33543da3ca0cd859dbf09e2ec65a1e4a6e05351c65de()
cdef extern from "varlen.h":
    object PyInit_e02cc06990a5ada3a85a18d319fd60b7cc78a9df61ff42e4786f4d38781487af()
cdef extern from "database.h":
    object PyInit_f49ae4fc6321b5716844fb825963c2777032e51a40f56f0503f3af1e3f8955c0()
cdef extern from "exceptions.h":
    object PyInit_b3acacb50dcc31991db99af96cbbc49276820ec09dea463248e530ed3c8ade75()
cdef extern from "iterators.h":
    object PyInit_e48e4f3fde6bac09965dfe16ba7482b2068a4443151253a3b333776762c00e3d()
cdef extern from "metadata.h":
    object PyInit_52813ff72b14112a0b4a03ad67bce8e14752f5412dcf659ec80ae4653d42b095()

cdef object get_definition_by_name(str name):
    if name == "tempsdb.series":
        return PyInit_03dbe33b62276c95dfcc6b35b29276d3c8f9eb00f1006964e2f49514eb537456()
    elif name == "tempsdb.chunks.maker":
        return PyInit_f16fd407cfbfb2ad452d52d2b745d1660ec3173e6bc8a2b02919498dbc99c5a7()
    elif name == "tempsdb.chunks.gzip":
        return PyInit_b7dee28f8f76409f72a74038ee6dd97f35b270b1992a243158290438c422783e()
    elif name == "tempsdb.chunks.direct":
        return PyInit_7e8c3d09a1c13dc99e4a4ac22f2fec9087991da8316365c6b6b626504e3e829a()
    elif name == "tempsdb.chunks.base":
        return PyInit_e4e05e6002b9e86a822bad12d8ff07494d560e0e6101b0d01364be04f15e053e()
    elif name == "tempsdb.chunks.normal":
        return PyInit_336fb6b6488526368c1e33543da3ca0cd859dbf09e2ec65a1e4a6e05351c65de()
    elif name == "tempsdb.varlen":
        return PyInit_e02cc06990a5ada3a85a18d319fd60b7cc78a9df61ff42e4786f4d38781487af()
    elif name == "tempsdb.database":
        return PyInit_f49ae4fc6321b5716844fb825963c2777032e51a40f56f0503f3af1e3f8955c0()
    elif name == "tempsdb.exceptions":
        return PyInit_b3acacb50dcc31991db99af96cbbc49276820ec09dea463248e530ed3c8ade75()
    elif name == "tempsdb.iterators":
        return PyInit_e48e4f3fde6bac09965dfe16ba7482b2068a4443151253a3b333776762c00e3d()
    elif name == "tempsdb.metadata":
        return PyInit_52813ff72b14112a0b4a03ad67bce8e14752f5412dcf659ec80ae4653d42b095()


cdef class CythonPackageLoader:
    cdef PyModuleDef* definition
    cdef object def_o
    cdef str name

    def __init__(self, name):
        self.def_o = get_definition_by_name(name)
        self.definition = <PyModuleDef*>self.def_o
        self.name = name
        Py_INCREF(self.def_o)

    def load_module(self, fullname):
        raise ImportError

    def create_module(self, spec):
        if spec.name != self.name:
            raise ImportError()
        return PyModule_FromDefAndSpec(self.definition, spec)

    def exec_module(self, module):
        PyModule_ExecDef(module, self.definition)


class CythonPackageMetaPathFinder:
    def __init__(self, modules_set):
        self.modules_set = modules_set

    def find_module(self, fullname, path):
        if fullname not in self.modules_set:
            return None
        return CythonPackageLoader(fullname)

    def invalidate_caches(self):
        pass

def bootstrap_cython_submodules():
    modules_set = {'tempsdb.varlen', 'tempsdb.chunks.maker', 'tempsdb.chunks.gzip', 'tempsdb.metadata', 'tempsdb.chunks.base', 'tempsdb.database', 'tempsdb.iterators', 'tempsdb.chunks.normal', 'tempsdb.chunks.direct', 'tempsdb.exceptions', 'tempsdb.series'}
    sys.meta_path.append(CythonPackageMetaPathFinder(modules_set))
