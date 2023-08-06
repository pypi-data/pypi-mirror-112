#pragma once
#pragma execution_character_set("utf-8")

#include "../core/relation.h"
#include <string>
#include <cstdint>
#include <vector>

using namespace SECYAN;

enum RelationName
{
    CUSTOMER,
    ORDERS,
    LINEITEM,
    PART,
    SUPPLIER,
    PARTSUPP,
    RTOTAL
};

enum QueryName{
    Q3,
    Q10,
    Q18,
    Q8,
    Q9,
    Q12,
    Q6,
    Q14,
    Q17,
    Q4,
    QTOTAL,
};

enum DataSize
{
    _1MB,
    _3MB,
    _10MB,
    _33MB,
    _100MB,
    DTOTAL
};

using run_query = void(DataSize, bool);
run_query run_Q3, run_Q10, run_Q18, run_Q8, run_Q9, run_Q12, run_Q16, run_Q1, run_Q4;