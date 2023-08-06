#include <Python.h>
#include <divsufsort.h>

static PyObject * _divsufsort(PyObject *self, PyObject *args)
{
    Py_buffer input;

    if (!PyArg_ParseTuple(args, "y*", &input))
        return nullptr;

    auto output = (saidx_t *)malloc(input.len * sizeof(saidx_t));
    if (!output)
        return PyErr_NoMemory();

    PyObject * r = nullptr;

    auto err = divsufsort((sauchar_t const *)input.buf, output, (saidx_t)input.len);
    if (err)
    {
        PyErr_Format(PyExc_RuntimeError, "divsufsort failed with %d", err);
        goto error;
    }

    r = PyTuple_New(input.len);
    if (!r)
        goto error;

    for (Py_ssize_t i = 0; i != input.len; ++i)
    {
        PyObject * idx = PyLong_FromSize_t(output[i]);
        if (!idx)
            goto error;
        if (PyTuple_SetItem(r, i, idx))
            goto error;
    }

    return r;

error:
    if (r)
        Py_XDECREF(r);
    free(output);
    return nullptr;
}

static PyMethodDef _methods[] = {
    {"divsufsort", &_divsufsort, METH_VARARGS, "Constructs the suffix array of a given bytes-like object" },
    {}
};

static PyModuleDef _module = {
    PyModuleDef_HEAD_INIT,
    "divsufsort",
    nullptr,
    -1,
    _methods,
};

extern "C" PyObject* PyInit_divsufsort()
{
    return PyModule_Create(&_module);
}
