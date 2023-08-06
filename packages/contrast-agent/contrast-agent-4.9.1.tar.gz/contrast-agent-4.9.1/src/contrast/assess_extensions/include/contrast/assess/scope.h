/*
* Copyright © 2021 Contrast Security, Inc.
* See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
*/
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>


typedef enum {
    CONTRAST_SCOPE = 0,
    PROPAGATION_SCOPE,
    TRIGGER_SCOPE,
    EVAL_SCOPE,
} ScopeLevel_t;


PyObject *enter_scope(PyObject *self, PyObject *args);
PyObject *exit_scope(PyObject *self, PyObject *args);
PyObject *in_scope(PyObject *self, PyObject *args);
PyObject *in_contrast_or_propagation_scope(PyObject *self, PyObject *args);
PyObject *set_thread_scope(PyObject *self, PyObject *thread_id);
PyObject *destroy_thread_scope(PyObject *self, PyObject *thread_id);
PyObject *get_thread_scope(PyObject *self, PyObject *args);

void enter_contrast_scope(void);
void exit_contrast_scope(void);
void enter_propagation_scope(void);
void exit_propagation_scope(void);
int should_propagate(void);
int in_eval_scope(void);
