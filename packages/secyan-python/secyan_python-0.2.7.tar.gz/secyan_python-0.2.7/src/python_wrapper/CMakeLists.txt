set(WRAPPER_NAME secyan_python)

# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")

find_package(pybind11 REQUIRED)
include_directories(${pybind11_INCLUDE_DIRS})
message([MAIN] "Found pybind11 v${pybind11_VERSION}: ${pybind11_INCLUDE_DIRS}")

find_package(Python3 COMPONENTS Interpreter Development)
include_directories(${Python3_INCLUDE_DIRS})
message([MAIN] "Found Python ${PythonLibs_VERSION}: ${Python3_INCLUDE_DIRS}")


pybind11_add_module(${WRAPPER_NAME} relation_wrapper.cpp secyan_python_wrapper.cpp party_wrapper.cpp)

target_compile_definitions(${WRAPPER_NAME} PRIVATE)

# Include python and python libraries to the target
# This one is required to write the wrapper
target_include_directories(${WRAPPER_NAME} PUBLIC ${Python3_INCLUDE_DIRS})
target_include_directories(${WRAPPER_NAME} PUBLIC ${Python3_LIBRARY_DIRS})


target_link_libraries(${WRAPPER_NAME}
        PUBLIC secyan
        PUBLIC ${Python3_LIBRARIES}
        )
