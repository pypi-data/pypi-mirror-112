# Install script for directory: /Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/relic" TYPE FILE FILES
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_alloc.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_arch.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_bc.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_bench.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_bn.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_core.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_cp.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_dv.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_eb.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_ec.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_ed.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_ep.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_epx.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_err.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_fb.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_fbx.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_fp.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_fpx.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_label.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_md.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_pc.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_pp.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_rand.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_test.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_types.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/relic_util.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/relic/low" TYPE FILE FILES
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/low/relic_bn_low.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/low/relic_dv_low.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/low/relic_fb_low.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/low/relic_fp_low.h"
    "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/include/low/relic_fpx_low.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/relic" TYPE DIRECTORY FILES "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/build/extern/ENCRYPTO_utils/extern/relic/include/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/extern/ENCRYPTO_utils/extern/relic/cmake/relic-config.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/Users/qiweili/Desktop/Project 1/SECYAN/extern/ABY/build/extern/ENCRYPTO_utils/extern/relic/src/cmake_install.cmake")

endif()

