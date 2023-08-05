//
//  observecallback.h
//  ingescapeWrapp
//
//  Created by vaugien on 12/02/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//
#include "observecallback.h"
#include <stdio.h>
#include <ingescape/ingescape.h>
#include "uthash/utlist.h"

#if (defined WIN32 || defined _WIN32)
#include "unixfunctions.h"
#endif

typedef struct observeCallback {
    char *nameArg;      // name of the iop
    PyObject *call;     //observeCallback
    PyObject *arglist;  //argument of the callback
    struct observeCallback *next;
    struct observeCallback *prev;
}observeCallback;
observeCallback *observeList = NULL;


//observeCallback that execute the callback for the iop that has benn changed
void observe(iop_t iopType, const char* name, iopType_t valueType, void* value, unsigned long valueSize, void* myData){
    // Lock the GIL to execute the callback safely
    PyGILState_STATE d_gstate;
    d_gstate = PyGILState_Ensure();
    //run through all callbacks to execute them
    observeCallback *actuel = NULL;
    PyObject *tupleArgs = PyTuple_New(5);
    PyTuple_SetItem(tupleArgs, 0, Py_BuildValue("i", iopType));
    PyTuple_SetItem(tupleArgs, 1, Py_BuildValue("s", name));
    PyTuple_SetItem(tupleArgs, 2, Py_BuildValue("i", valueType));

    DL_FOREACH(observeList, actuel){
        if (strcmp(actuel->nameArg, name) == 0){
            switch(valueType){
                case IGS_BOOL_T:
                    if (*(bool*)value){
                        PyTuple_SetItem(tupleArgs, 3, Py_True);
                    }else{
                        PyTuple_SetItem(tupleArgs, 3, Py_False);
                    }
                    break;
                case IGS_INTEGER_T:
                    PyTuple_SetItem(tupleArgs, 3, Py_BuildValue("i", *(int*)value));
                    break;
                case IGS_DOUBLE_T:
                    PyTuple_SetItem(tupleArgs, 3, Py_BuildValue("d", *(double*)value));
                    break;
                case IGS_STRING_T:
                    PyTuple_SetItem(tupleArgs, 3, Py_BuildValue("s", (char*)value));
                    break;
                case IGS_IMPULSION_T:
                    PyTuple_SetItem(tupleArgs, 3, Py_None);
                    break;
                case IGS_DATA_T:
                    PyTuple_SetItem(tupleArgs, 3, Py_BuildValue("y#", value, valueSize));
                    break;
                case IGS_UNKNOWN_T:
                    break;
            }
            Py_XINCREF(actuel->arglist);
            PyTuple_SetItem(tupleArgs, 4, actuel->arglist);
            PyObject *KWARGS = NULL;
            PyObject_Call(actuel->call, tupleArgs, KWARGS);
            Py_XDECREF(tupleArgs);
            Py_XDECREF(KWARGS);
        }
    }
    //release the GIL
    PyGILState_Release(d_gstate);
}

PyObject * igs_observeInput_wrapper(PyObject *self, PyObject *args)
{
    PyObject *temp;
    PyObject *temparglist;
    PyObject *arg;
    char *input;
    
    // parse the callback and arguments sent from python
    if (PyArg_ParseTuple(args, "sOO", &input, &temp, &arg)) {
        if (!PyCallable_Check(temp)) {      // check if the callback is a function
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
    }
    Py_XINCREF(temp);       // Add a reference to new callback
    temparglist = Py_BuildValue("O", arg);    //cast arglist into a tuple
    
    // add the callback to the list of Callback
    observeCallback *newElt = calloc(1, sizeof(observeCallback));
    newElt->nameArg = strndup(input, strlen(input));
    newElt->arglist = temparglist;
    newElt->call = temp;
    DL_APPEND(observeList, newElt);
    igs_observeInput(input, observe, input);
    return PyLong_FromLong(0);
    
}

PyObject * igs_observeOutput_wrapper(PyObject *self, PyObject *args)
{
    PyObject *temp;
    PyObject *temparglist;
    PyObject *arg;
    char *output;
    
    // parse the callback and arguments sent from python
    if (PyArg_ParseTuple(args, "sOO", &output, &temp, &arg)) {
        if (!PyCallable_Check(temp)) {      // check if the callback is a function
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
    }
    
    Py_XINCREF(temp);         // Add a reference to new callback
    temparglist = Py_BuildValue("O", arg);    //cast arglist into a tuple
    
    // add the callback to the list of Callback
    observeCallback *newElt = calloc(1, sizeof(observeCallback));
    newElt->nameArg = strndup(output, strlen(output));
    newElt->arglist = temparglist;
    newElt->call = temp;
    DL_APPEND(observeList, newElt);
    igs_observeOutput(output, observe, output);
    return PyLong_FromLong(0);
}

PyObject * igs_observeParameter_wrapper(PyObject *self, PyObject *args)
{
    PyObject *temp;
    PyObject *temparglist;
    PyObject *arg;
    char *param;
    
    // parse the callback and arguments sent from python
    if (PyArg_ParseTuple(args, "sOO", &param, &temp, &arg)) {
        if (!PyCallable_Check(temp)) {      // check if the callback is a function
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
    }
    
    Py_XINCREF(temp);         // Add a reference to new callback
    temparglist = Py_BuildValue("O", arg);        //cast arglist into a tuple
    
    // add the callback to the list of Callback
    observeCallback *newElt = calloc(1, sizeof(observeCallback));
    newElt->nameArg = strndup(param, strlen(param));
    newElt->arglist = temparglist;
    newElt->call = temp;
    DL_APPEND(observeList, newElt);
    igs_observeParameter(param, observe, param);
    return PyLong_FromLong(0);
}

