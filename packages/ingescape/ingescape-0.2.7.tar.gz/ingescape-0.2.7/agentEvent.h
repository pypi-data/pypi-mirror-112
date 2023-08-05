//
//  agentEvent.h
//  ingescapeWrapp
//
//  Created by vaugien on 01/07/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#ifndef agentEvent_h
#define agentEvent_h

#include <stdio.h>
#include <Python.h>

// wrapper for igs_observeAgentEvents
PyObject * igs_observeAgentEvents_wrapper(PyObject *self, PyObject *args);

#endif /* agentEvent_h */