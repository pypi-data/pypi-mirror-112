#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "pcre.h"
#include "Textifier.h"
#include <iostream>
#include "utilities.h"


typedef struct {
    PyObject_HEAD
    Textifier *textifier;
} TextifierObject;

static void
Textifier_dealloc(TextifierObject *self)
{
  delete self->textifier;
  Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *
Textifier_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    TextifierObject *self;

    self = (TextifierObject *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->textifier = NULL;
    }

    return (PyObject *)self;
}

static int
Textifier_init(TextifierObject *self, PyObject *args, PyObject *kwds)
{
    self->textifier = new Textifier();
    return NULL;
}

static PyObject *Textifier_textify(TextifierObject* self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"input", NULL};
    PyObject *input = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O", kwlist, &input)) {
        return NULL;
    }

    if (!PyUnicode_Check(input)) {
        PyErr_SetString(PyExc_RuntimeError, "Input must be a string");
        return NULL;
    }

    Py_ssize_t len;
    const char* input_chars = PyUnicode_AsUTF8AndSize(input, &len);

    char* output_chars = new char[2*len+1]; // not sure why it needs to be so big (2*l+1), but matches the command line version

    PyObject* output = NULL;

    try {
      int output_len = self->textifier->textify(input_chars, len, output_chars, len);
      output_chars[output_len] = NULL; // terminate string

      output = PyUnicode_FromFormat("%s", output_chars);
    } catch (Error ex) {
        PyObject* err = Py_BuildValue("(si)", ex.message.c_str(), ex.pos);
        PyErr_SetObject(PyExc_ValueError, err);
        Py_DECREF(err); // now owned by PyErr
    }

    delete output_chars;
    return output;
}

static PyMethodDef Textifier_methods[] = {
    {"textify", (PyCFunction) Textifier_textify, METH_VARARGS | METH_KEYWORDS,
     "Remove wiki markup from text"},
    {NULL}  /* Sentinel */
};

static PyTypeObject TextifierType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pyautocorpus.Textifier",  /* tp_name */
    sizeof(TextifierObject),   /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor) Textifier_dealloc, /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    0,                         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "autocorpus wikipedia textifier", /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    Textifier_methods,         /* tp_methods */
    0,                         /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)Textifier_init,  /* tp_init */
    0,                         /* tp_alloc */
    Textifier_new,             /* tp_new */
};

static PyMethodDef PyAutoCorpusMethods[] = {
    {NULL, NULL, 0, NULL}
};

static PyModuleDef pyautocorpus_module = {
    PyModuleDef_HEAD_INIT,
    "pyautocorpus",
    "c++ extensions for AutoCorpus",
    -1,
    PyAutoCorpusMethods
};

PyMODINIT_FUNC
PyInit_pyautocorpus(void)
{
    PyObject *m;

    if (PyType_Ready(&TextifierType) < 0)
        return NULL;

    m = PyModule_Create(&pyautocorpus_module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&TextifierType);
    if (PyModule_AddObject(m, "Textifier", (PyObject *) &TextifierType) < 0) {
      Py_DECREF(&TextifierType);
      Py_DECREF(m);
      return NULL;
    }

    return m;
}
