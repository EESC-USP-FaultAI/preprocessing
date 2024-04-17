#include <Python.h>
#include <numpy/arrayobject.h>

#define PI 3.14159265358979323846

typedef struct {
    double real;
    double imag;
} complex;

static void fft(complex* input, int N){
    if (N <= 1) return;
    complex *even = (complex*) malloc(N/2 * sizeof(complex));
    complex *odd = (complex*) malloc(N/2 * sizeof(complex));

    for (int i = 0; i < N/2; ++i) {
        even[i] = input[2*i];
        odd[i] = input[2*i + 1];
    }

    fft(even, N/2);
    fft(odd, N/2);

    complex aux;
    double angle, cos_val, sin_val;
    for (int i = 0; i < N/2; ++i) {
        
        angle = - 2 * Py_MATH_PI * i / N;
        cos_val = cos(angle);
        sin_val = sin(angle);
        
        aux.real = cos_val * odd[i].real - sin_val * odd[i].imag;
        aux.imag = cos_val * odd[i].imag + sin_val * odd[i].real;
        
        input[i].real = even[i].real + aux.real;
        input[i].imag = even[i].imag + aux.imag;
        
        input[i + N/2].real = even[i].real - aux.real;
        input[i + N/2].imag = even[i].imag - aux.imag;
    }
    free(even);
    free(odd);
}

static void fft_inplace(complex* input, int N, int inverse){
    int i, j, k, m;
    complex u, w, t;

    #pragma omp parallel for private(j, t)
    for (i = 0; i < N; i++) {
        j = 0;
        for (k = 1; k < N; k <<= 1) {
            j = (j << 1) | (i & k ? 1 : 0);
        }
        if (i < j) {
            t = input[i];
            input[i] = input[j];
            input[j] = t;
        }
    }

    for (m = 2; m <= N; m <<= 1) {
        double p = inverse ? PI / (m >> 1) : -PI / (m >> 1);
        w.real = cos(p);
        w.imag = sin(p);
        #pragma omp parallel for private(j, u, t)
        for (k = 0; k < N; k += m) {
            u.real = 1.0;
            u.imag = 0.0;
            for (j = 0; j < m >> 1; j++) {
                t.real = input[k + j + (m >> 1)].real * u.real - input[k + j + (m >> 1)].imag * u.imag;
                t.imag = input[k + j + (m >> 1)].real * u.imag + input[k + j + (m >> 1)].imag * u.real;
                input[k + j + (m >> 1)].real = input[k + j].real - t.real;
                input[k + j + (m >> 1)].imag = input[k + j].imag - t.imag;
                input[k + j].real += t.real;
                input[k + j].imag += t.imag;
                double temp = u.real * w.real - u.imag * w.imag;
                u.imag = u.real * w.imag + u.imag * w.real;
                u.real = temp;
            }
        }
    }
    if (inverse) {
        #pragma omp parallel for
        for (i = 0; i < N; i++) {
            input[i].real /= N;
            input[i].imag /= N;
        }
    }
}

static PyObject* py_fft(PyObject *self, PyObject *args){

    PyObject *py_input = NULL;

    // Get the input ref as python object
    PyArg_ParseTuple(args, "O|i", &py_input);

    // Get the input as numpy array
    PyArrayObject* np_input = (PyArrayObject*)PyArray_FROM_OTF(py_input, NPY_COMPLEX128, NPY_ARRAY_IN_ARRAY);

    // Get the dimensions of the input array
    int* dims = (int*) PyArray_DIMS(np_input);
    // Get the input data as C Array
    complex* c_input = (complex*)PyArray_DATA(np_input);

    // Call the fft function
    fft(c_input, dims[0]);

    // Return the output as numpy array
    return PyArray_Return(np_input);
}

static PyObject* py_fft_inPlace(PyObject *self, PyObject *args){

    PyObject *py_input = NULL;

    // Get the input ref as python object
    PyArg_ParseTuple(args, "O|i", &py_input);

    // Get the input as numpy array
    PyArrayObject* np_input = (PyArrayObject*)PyArray_FROM_OTF(py_input, NPY_COMPLEX128, NPY_ARRAY_IN_ARRAY);

    // Get the dimensions of the input array
    int* dims = (int*) PyArray_DIMS(np_input);
    // Get the input data as C Array
    complex* c_input = (complex*)PyArray_DATA(np_input);

    // Call the fft function
    fft_inplace(c_input, dims[0], 0);

    // Return the output as numpy array
    return PyArray_Return(np_input);
}

static PyMethodDef fft_c_methods[] = {
    {"fft", py_fft, METH_VARARGS, "Fast Fourier Transform"},
    {"fft_inplace", py_fft_inPlace, METH_VARARGS, "Fast Fourier Transform Inplace"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module_definition = {
    PyModuleDef_HEAD_INIT,
    "Fourier",
    "Fourier Transform Module",
    -1,
    fft_c_methods
};

PyMODINIT_FUNC PyInit_fft_c(void){
    import_array();
    return PyModule_Create(&module_definition);
}


