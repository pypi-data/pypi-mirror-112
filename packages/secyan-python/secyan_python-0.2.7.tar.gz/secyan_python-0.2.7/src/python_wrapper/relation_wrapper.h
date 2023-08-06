//
// Created by Qiwei Li on 6/10/21.
//
#include <pybind11/pybind11.h>
#include "Python.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <algorithm>
#include "circuit/share.h"
#include "../core/relation.h"
#include "../core/party.h"


namespace py = pybind11;

void init_relationship(py::module &m);
void init_DataType(py::module &m);
void init_e_role(py::module &m);
void init_relation_info(py::module &m);
void init_annot_info(py::module &m);
void init_date_time(py::module &m);

