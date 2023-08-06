# Basic CMake file to compile components
#
# To compile, run:
# - mkdir build && cd build
# - cmake ..
# - make
# Optionally, to install:
# - sudo make install

# CMake minimum version of 2.8 required
cmake_minimum_required (VERSION 2.8)

# Raise fatal error if version not met cmake_minimum_required (VERSION 2.8 FATAL_ERROR)

# get pkg-config
# TODO: Find out whether we actually have to use pkg-config
find_package(PkgConfig REQUIRED)

# Name project and set to C++ Project
project ({{ project_name }} CXX)
# Set the project source dir (just convention)
set( PROJECT_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR} )
set( PROJECT_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR} )

# Set version of project
set (PROJECT_VERSION_MAJOR 0)
set (PROJECT_VERSION_MINOR 1)
set (PROJECT_VERSION_PATCH 0)

# Check for package using pkg-config - GTKMM here is an example package (require v3.0 or greater)
pkg_check_modules(GTKMM REQUIRED gtkmm-3.0>=3.0)

# Include directories
include_directories(include)

# any additional libs
set( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/CMake/modules/" )

# Setup source files
set({{ project_name }}_SOURCES
	 src/main.cpp
)

# Set compiler
add_executable ( ${PROJECT_NAME} ${__PROJ_SOURCES})

# Link libs
target_link_libraries ( ${PROJECT_NAME} ${GTKMM_LIBRARIES} m)
target_include_directories ( ${PROJECT_NAME} PUBLIC ${GTKMM_INCLUDE_DIRS})
target_compile_options ( ${PROJECT_NAME} PUBLIC ${GTKMM_CFLAGS_OTHER})

# Compiler Condition (gcc ; g++)
if ( "${CMAKE_C_COMPILER_ID}" STREQUAL "GNU" )
  message( STATUS "Setting the flags for ${CMAKE_C_COMPILER_ID} compiler" )
  add_definitions( --std=c99 )
endif()

# Check for OS
if( UNIX )
	set( PROJECT_DEFINITIONS
	    "${PROJECT_DEFINITIONS} -Wall -Wextra -Werror -Wno-deprecated-declarations -Wno-unused-parameter -Wno-comment" )
endif()

