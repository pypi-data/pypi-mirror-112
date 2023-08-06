#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#define MI_MODULE_NAME "_attrdict"
#define SENTINEL {NULL}

typedef struct {
    PyDictObject dict;
} Mi_AttrDict_Object;

static PyTypeObject Mi_AttrDict_Type;

PyObject *
Mi_AttrDict_Getattr(PyObject *self, PyObject *attr) {
    PyObject *value = NULL;

    value = PyDict_GetItemWithError(self, attr); // borrowed ref
    if (value == NULL) {
        PyErr_SetObject(PyExc_AttributeError, attr);
        goto error;
    }

    Py_INCREF(value);

    if (!PyObject_IsInstance(value, (PyObject *) &Mi_AttrDict_Type) && PyDict_Check(value)) {
        #define nargsf 1
        PyObject *const args[nargsf] = {value};
        PyObject *new_value = PyObject_Vectorcall((PyObject *) &Mi_AttrDict_Type, args, nargsf, NULL);
        #undef nargsf

        Py_DECREF(value);
        value = new_value;
        if (PyDict_SetItem(self, attr, value) < 0) {
            goto cleanup;
        }
    }

    return value;

cleanup:
    Py_XDECREF(value);
error:
    return NULL;
}

PyObject *
Mi_AttrDict_Getattribute(PyObject *self, PyObject *attr) {
    PyObject *value = NULL;

    value = _PyObject_GenericGetAttrWithDict(self, attr, NULL, 1); // new ref
    if (value == NULL) {
        value = Mi_AttrDict_Getattr(self, attr);
    }

    return value;
}

int
Mi_AttrDict_Setattr(PyObject *self, PyObject *attr, PyObject *value) {
    return PyDict_SetItem(self, attr, value);
}

static PyMethodDef Mi_AttrDict_Methods[] = {
    {"__getattr__", (PyCFunction) Mi_AttrDict_Getattr, METH_O, PyDoc_STR("__getattr__")},
    SENTINEL,
};

static PyTypeObject Mi_AttrDict_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    .tp_name = MI_MODULE_NAME ".AttrDict",
    .tp_basicsize = sizeof(Mi_AttrDict_Object),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_DICT_SUBCLASS,
    .tp_methods = Mi_AttrDict_Methods,
    .tp_getattro = Mi_AttrDict_Getattribute,
    .tp_setattro = Mi_AttrDict_Setattr,
};

static PyMethodDef Mi_Methods[] = {
    SENTINEL,
};

static struct PyModuleDef Mi_Module = {
    PyModuleDef_HEAD_INIT,
    .m_name = MI_MODULE_NAME,
    .m_doc = NULL,
    .m_size = -1,
    Mi_Methods,
};

PyMODINIT_FUNC
PyInit__attrdict(void) {
    PyObject *module;

    #define Mi_Type_Ready(type) \
        do { \
            if (PyType_Ready(type) < 0) {\
                return NULL; \
            } \
        } while(0);
    #define Mi_Module_AddObject(name, type) \
        do { \
            Py_INCREF(type); \
            if (PyModule_AddObject(module, name, (PyObject *) type) < 0) { \
                goto error; \
            } \
        } while(0);

    Mi_AttrDict_Type.tp_base = &PyDict_Type;
    Mi_Type_Ready(&Mi_AttrDict_Type)

    module = PyModule_Create(&Mi_Module);
    if (module == NULL) {
        goto error;
    }

    Mi_Module_AddObject("AttrDict", &Mi_AttrDict_Type);

    #undef Mi_Type_Ready
    #undef Mi_Module_AddObject

    return module;

error:
    Py_XDECREF(&Mi_AttrDict_Type);
    Py_XDECREF(module);
    return NULL;
}
