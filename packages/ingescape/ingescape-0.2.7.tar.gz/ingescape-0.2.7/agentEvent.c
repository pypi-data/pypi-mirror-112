//
//  agentEvent.c
//  ingescapeWrapp
//
//  Created by vaugien on 01/07/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#include "agentEvent.h"
#include <ingescape/ingescape_advanced.h>
#include "uthash/utlist.h"

typedef struct agentEventCallback{
    PyObject *call;         //stopCallback
    PyObject *argList;  // argument for stopCallback
    struct agentEventCallback *next;
    struct agentEventCallback *prev;
}agentEventCallback;

agentEventCallback *agentEventCallbackList = NULL;

void onAgentEvent(igs_agent_event_t event, const char *uuid, const char *name, void *eventData, void *myData){
    //run through all callbacks to execute them

    agentEventCallback *currentCallback = NULL;
    DL_FOREACH(agentEventCallbackList, currentCallback){
        // Lock the GIL to execute the callback safely
        PyGILState_STATE d_gstate;
        d_gstate = PyGILState_Ensure();
        PyObject *globalArgList = NULL;
        if (eventData){
            
            globalArgList = PyTuple_Pack(5, PyLong_FromLong(event)
                                            , Py_BuildValue("s",uuid)
                                            , Py_BuildValue("s",name)
                                            , Py_BuildValue("s",(char*)eventData)
                                            , currentCallback->argList);
        }else{
            globalArgList = PyTuple_Pack(5, PyLong_FromLong(event)
                                            , Py_BuildValue("s",uuid)
                                            , Py_BuildValue("s",name)
                                            , Py_None
                                            , currentCallback->argList);
        }

        Py_XINCREF(globalArgList);

        //execute the callback
        PyObject_CallObject(currentCallback->call, globalArgList);
        //release the GIL
        PyGILState_Release(d_gstate);
    }
}

PyObject * igs_observeAgentEvents_wrapper(PyObject *self, PyObject *args)
{
    PyObject *temp;
    PyObject arg;
    PyObject *tempargList;

    // parse the callback and arguments sent from python
    if (PyArg_ParseTuple(args, "OO", &temp, &arg)) {
        if (!PyCallable_Check(temp)) {  // check if the callback is a function
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
    }
    
    Py_XINCREF(temp);               // Add a reference to new callback
    
    tempargList = Py_BuildValue("O", arg); 
    
    Py_XINCREF(tempargList);    // Add a reference to arglist

    // add the callback to the list of agentEventCallback
    agentEventCallback *newElt = calloc(1, sizeof(agentEventCallback));
    newElt->argList = tempargList;
    newElt->call = temp;
    DL_APPEND(agentEventCallbackList, newElt);
    
    igs_observeAgentEvents(onAgentEvent, NULL);
    return PyLong_FromLong(1);
}