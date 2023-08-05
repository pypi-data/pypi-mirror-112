#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "pcre.h"
#include "Textifier.h"
#include <iostream>




static PyObject *textify(PyObject* self, PyObject *args, PyObject *kwds)
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

    char* output_chars = new char[len];

    Textifier* textifier = new Textifier();

    int output_len = textifier->textify(input_chars, len, output_chars, len);

    output_chars[output_len] = NULL; // terminate string

    PyObject *output = PyUnicode_FromFormat("%s", output_chars);

    delete output_chars;
    delete textifier;

    return output;
}


static PyMethodDef PyAutoCorpusMethods[] = {
    {"textify", (PyCFunction) textify, METH_VARARGS | METH_KEYWORDS, "textify"},
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

    m = PyModule_Create(&pyautocorpus_module);
    if (m == NULL)
        return NULL;

    return m;
}
