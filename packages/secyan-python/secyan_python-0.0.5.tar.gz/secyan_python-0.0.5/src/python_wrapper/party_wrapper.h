//
// Created by Qiwei Li on 6/10/21.
//
#include <pybind11/pybind11.h>
#include "Python.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <algorithm>
#include "circuit/share.h"
#include "../core/party.h"


namespace py = pybind11;

void init_party(py::module &m);