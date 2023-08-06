//
// Created by Qiwei Li on 6/10/21.
//

#include "relation_wrapper.h"
#include "party_wrapper.h"

namespace py = pybind11;


PYBIND11_MODULE(secyan_python, m) {
    init_relation_info(m);
    init_annot_info(m);
    init_relationship(m);

    init_party(m);
    py::module utils = m.def_submodule("utils", "A module contains list of helper functions");
    utils.def("init_global_party", &SECYAN::initGlobalParty, py::arg("address"), py::arg("port"), py::arg("role"));
    init_date_time(utils);

    py::module constant = m.def_submodule("constant", "A module contains list of constant values");
    init_e_role(constant);
    init_DataType(constant);

}

