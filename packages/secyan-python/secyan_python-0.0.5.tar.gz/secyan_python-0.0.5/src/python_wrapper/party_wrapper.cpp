//
// Created by Qiwei Li on 6/10/21.
//

#include "party_wrapper.h"


namespace py = pybind11;

void init_party(py::module &m) {
    py::class_<SECYAN::Party>(m, "Party")
            .def(py::init())
            .def("init", &SECYAN::Party::Init)
          ;

}