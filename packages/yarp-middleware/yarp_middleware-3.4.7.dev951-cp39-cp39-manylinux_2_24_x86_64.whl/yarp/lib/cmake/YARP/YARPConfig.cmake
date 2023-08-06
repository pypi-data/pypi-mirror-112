# SPDX-FileCopyrightText: 2006-2021 Istituto Italiano di Tecnologia (IIT)
# SPDX-FileCopyrightText: 2006-2010 RobotCub Consortium
# SPDX-License-Identifier: BSD-3-Clause



include(CMakeDependentOption)


# Version
set(YARP_VERSION_MAJOR "3")
set(YARP_VERSION_MINOR "4")
set(YARP_VERSION_PATCH "102")
set(YARP_VERSION_TWEAK "")
set(YARP_VERSION "3.4.102+20210713.25+git88f97f3c8")
set(YARP_VERSION_SHORT "3.4.102")

# Build type and flags
set(YARP_IS_SHARED_LIBRARY OFF)

set(YARP_C_COMPILER_ID "Clang")
set(YARP_C_COMPILER_VERSION "7.0.1")
set(YARP_C_FLAGS " ")

set(YARP_CXX_COMPILER_ID "Clang")
set(YARP_CXX_COMPILER_VERSION "7.0.1")
set(YARP_CXX_FLAGS " -Wall -Wextra -Wsign-compare -Wpointer-arith -Winit-self -Wnon-virtual-dtor -Wcast-align -Wunused -Wvla -Wmissing-include-dirs -Wreorder -Wsizeof-pointer-memaccess -Woverloaded-virtual -Wtautological-undefined-compare -Wmismatched-new-delete -Wparentheses-equality -Wundef -Wredundant-decls -Wunknown-pragmas -Wunused-result -Wc++17-compat -Wc++2a-compat -Wheader-guard -Wignored-attributes -Wnewline-eof -Wdangling-else -Wgcc-compat -Wmicrosoft-exists -Wstatic-inline-explicit-instantiation -Wtautological-compare -Winconsistent-missing-override -Wnull-conversion  -Wno-unused-parameter  -Wdeprecated-declarations ")



####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was YARPConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################


# Check if deprecated methods are built
set(YARP_NO_DEPRECATED OFF)
if(YARP_NO_DEPRECATED)
  add_definitions("-DYARP_NO_DEPRECATED")
else(YARP_NO_DEPRECATED)
  set(YARP_BINDINGS "${PACKAGE_PREFIX_DIR}/share/yarp/bindings")
endif(YARP_NO_DEPRECATED)

# Disable deprecated warnings, but add an option to enable it
cmake_dependent_option(YARP_NO_DEPRECATED_WARNINGS
                       "Do not warn when using YARP deprecated declarations" FALSE
                       "NOT YARP_NO_DEPRECATED" FALSE)
mark_as_advanced(YARP_NO_DEPRECATED_WARNINGS)
if(YARP_NO_DEPRECATED_WARNINGS)
  add_definitions("-DYARP_NO_DEPRECATED_WARNINGS")
endif()


# Install prefix
set(YARP_INSTALL_PREFIX "${PACKAGE_PREFIX_DIR}")

# Directory containing CMake config files for other exports
set(YARP_CMAKECONFIG_DIR "${PACKAGE_PREFIX_DIR}/lib/cmake")

# Install directories (relative path)
set(YARP_DATA_INSTALL_DIR "share/yarp")
set(YARP_CONFIG_INSTALL_DIR "share/yarp/config")
set(YARP_PLUGIN_MANIFESTS_INSTALL_DIR "share/yarp/plugins")
set(YARP_MODULES_INSTALL_DIR "share/yarp/modules")
set(YARP_APPLICATIONS_INSTALL_DIR "share/yarp/applications")
set(YARP_TEMPLATES_INSTALL_DIR "share/yarp/templates")
set(YARP_APPLICATIONS_TEMPLATES_INSTALL_DIR "share/yarp/templates/applications")
set(YARP_MODULES_TEMPLATES_INSTALL_DIR "share/yarp/templates/modules")
set(YARP_CONTEXTS_INSTALL_DIR "share/yarp/contexts")
set(YARP_ROBOTS_INSTALL_DIR "share/yarp/robots")
set(YARP_STATIC_PLUGINS_INSTALL_DIR "lib")
set(YARP_DYNAMIC_PLUGINS_INSTALL_DIR "lib/yarp")
set(YARP_QML2_IMPORT_DIR "lib/qt5/qml")

# Install directories (absolute path)
set_and_check(YARP_DATA_INSTALL_DIR_FULL "${PACKAGE_PREFIX_DIR}/share/yarp")
set(YARP_CONFIG_INSTALL_DIR_FULL "${PACKAGE_PREFIX_DIR}/share/yarp/config")
set(YARP_PLUGIN_MANIFESTS_INSTALL_DIR_FULL "${PACKAGE_PREFIX_DIR}/share/yarp/plugins")
set(YARP_MODULES_INSTALL_DIR_FULL "${PACKAGE_PREFIX_DIR}/share/yarp/modules")
set(YARP_APPLICATIONS_INSTALL_DIR_FULL "${PACKAGE_PREFIX_DIR}/share/yarp/applications")
set(YARP_TEMPLATES_INSTALL_DIR_FULL "${PACKAGE_PREFIX_DIR}/share/yarp/templates")
set(YARP_APPLICATIONS_TEMPLATES_INSTALL_DIR_FULL "${PACKAGE_PREFIX_DIR}/share/yarp/templates/applications")
set(YARP_MODULES_TEMPLATES_INSTALL_DIR_FULL "${PACKAGE_PREFIX_DIR}/share/yarp/templates/modules")
set(YARP_CONTEXTS_INSTALL_DIR_FULL "${PACKAGE_PREFIX_DIR}/share/yarp/contexts")
set(YARP_ROBOTS_INSTALL_DIR_FULL "${PACKAGE_PREFIX_DIR}/share/yarp/robots")
set(YARP_STATIC_PLUGINS_INSTALL_DIR_FULL "${PACKAGE_PREFIX_DIR}/lib")
set(YARP_DYNAMIC_PLUGINS_INSTALL_DIR_FULL "${PACKAGE_PREFIX_DIR}/lib/yarp")
set(YARP_QML2_IMPORT_DIR_FULL "${PACKAGE_PREFIX_DIR}/lib/qt5/qml")

# Used by YarpIDL.cmake
set(YARP_IDL_BINARY_HINT "${PACKAGE_PREFIX_DIR}/bin")

# CMake modules directories
set_and_check(YARP_MODULE_DIR "${PACKAGE_PREFIX_DIR}/share/yarp/cmake")

# Save the variables, that it should not be modified by find_package(YARP), but
# we need to modify it in order to find all the dependencies.
set(_CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH})
set(_YCM_FOUND ${YCM_FOUND})

# Find YCM if YARP is static therefore we need YCM (or YARP private version) for
# private dependencies.
if(NOT YARP_IS_SHARED_LIBRARY)
  include(CMakeFindDependencyMacro)
  find_dependency(YCM 0.13.0 REQUIRED)
endif()


if(YARP_FIND_COMPONENTS STREQUAL "")
  # No components requested.
  # Search for the main YARP libraries only.
  set(YARP_FIND_COMPONENTS os;sig;dev;idl_tools)
endif()

# Find all requested components
set(YARP_LIBRARIES YARP::YARP_init)
foreach(_yarp_component ${YARP_FIND_COMPONENTS})

  if(NOT YARP_NO_DEPRECATED) # Since YARP 3.3
    set(_yarp_component_is_uppercase_os 0)
    if("${_yarp_component}" STREQUAL "OS")
      message(DEPRECATION "The 'OS' component is deprecated. Use 'os' instead, and replace YARP::YARP_OS with YARP::YARP_os.")
      set(_yarp_component_is_uppercase_os 1)
      set(_yarp_component os)
    endif()
  endif()

  set(_YARP_FIND_PART_${_yarp_component}_REQUIRED)
  # Only propagate REQUIRED if module was not passed to OPTIONAL_COMPONENTS
  if(YARP_FIND_REQUIRED AND YARP_FIND_REQUIRED_${_yarp_component})
    set(_YARP_FIND_PART_${_yarp_component}_REQUIRED REQUIRED)
  endif()
  set(_YARP_FIND_PARTS_QUIET)
  if(YARP_FIND_QUIETLY)
    set(_YARP_FIND_PARTS_QUIET QUIET)
  endif()
  get_property(_yarp_${_yarp_component}_transitive_dependency_set GLOBAL PROPERTY _CMAKE_YARP_${_yarp_component}_TRANSITIVE_DEPENDENCY SET)
  find_package(YARP_${_yarp_component}
               ${_YARP_FIND_PARTS_QUIET}
               ${_YARP_FIND_PART_${_yarp_component}_REQUIRED}
               HINTS "${YARP_CMAKECONFIG_DIR}"
               NO_DEFAULT_PATH)
  # Ensure that YARP components are not shown by FeatureSummary if not requested
  # by the user
  if(NOT _yarp_${_yarp_component}_transitive_dependency_set)
    set_property(GLOBAL PROPERTY _CMAKE_YARP_${_yarp_component}_TRANSITIVE_DEPENDENCY TRUE)
  endif()
  if(YARP_${_yarp_component}_FOUND AND TARGET YARP::YARP_${_yarp_component})
    list(APPEND YARP_LIBRARIES YARP::YARP_${_yarp_component})
  endif()

  if(NOT YARP_NO_DEPRECATED) # Since YARP 3.3
    if(_yarp_component_is_uppercase_os)
      set(YARP_OS_FOUND ${YARP_os_FOUND})
    endif()
  endif()
endforeach()

# Restore the original value of the variables
set(CMAKE_MODULE_PATH ${_CMAKE_MODULE_PATH})
set(YCM_FOUND ${_YCM_FOUND})
unset(_CMAKE_MODULE_PATH)
unset(_YCM_FOUND)


# Ensure that all requested modules are available
check_required_components(YARP)


################################################################################
# Load CMake helper functions

include(${YARP_MODULE_DIR}/YarpPlugin.cmake)
include(${YARP_MODULE_DIR}/YarpInstallationHelpers.cmake)


################################################################################
# If FeatureSummary was included, add DESCRIPTION and URL

if(COMMAND set_package_properties)
    set_package_properties(YARP PROPERTIES DESCRIPTION "A library and toolkit for communication and device interfaces"
                                           URL "https://www.yarp.it/")
endif()


################################################################################
# Print YARP information

if(NOT YCM_FIND_QUIETLY)
  message(STATUS "Found YARP: ${YARP_DIR} (found version \"${YARP_VERSION}\")")
endif()


################################################################################
# Deprecated variables

if(NOT YARP_NO_DEPRECATED AND NOT COMMAND _YARP_DEPRECATED_VARIABLE_WARNING)

  # A macro to print a warning when using deprecated variables, called by
  # variable_watch
  macro(_YARP_DEPRECATED_VARIABLE_WARNING _variable)
    message(DEPRECATION "The ${_variable} variable is deprecated")
  endmacro()

  # YARP_os_LIBRARY is deprecated since YARP 3.0.0
  set(YARP_os_LIBRARY YARP::YARP_os)
  variable_watch(YARP_os_LIBRARY _yarp_deprecated_variable_warning)

  # YARP_OS_LIBRARY is deprecated since YARP 3.0.0
  set(YARP_OS_LIBRARY YARP::YARP_os)
  variable_watch(YARP_OS_LIBRARY _yarp_deprecated_variable_warning)

  # YARP_SIG_LIBRARY is deprecated since YARP 3.0.0
  set(YARP_SIG_LIBRARY YARP::YARP_sig)
  variable_watch(YARP_SIG_LIBRARY _yarp_deprecated_variable_warning)

  # YARP_MATH_LIBRARY is deprecated since YARP 3.0.0
  if(TARGET YARP::YARP_math)
    set(YARP_MATH_LIBRARY YARP::YARP_math)
  endif()
  variable_watch(YARP_MATH_LIBRARY _yarp_deprecated_variable_warning)

  # YARP_DEV_LIBRARY is deprecated since YARP 3.0.0
  set(YARP_DEV_LIBRARY YARP::YARP_dev)
  variable_watch(YARP_DEV_LIBRARY _yarp_deprecated_variable_warning)

  # YARP_NAME_LIBRARY is deprecated since YARP 3.0.0
  if(TARGET YARP::YARP_name)
    set(YARP_NAME_LIBRARY YARP::YARP_name)
  endif()
  variable_watch(YARP_NAME_LIBRARY _yarp_deprecated_variable_warning)

  # YARP_INIT_LIBRARY is deprecated since YARP 3.0.0
  set(YARP_INIT_LIBRARY YARP::YARP_init)
  variable_watch(YARP_INIT_LIBRARY _yarp_deprecated_variable_warning)

  # YARP_HAS_MATH_LIB is deprecated since YARP 3.0.0
  set(YARP_HAS_MATH_LIB FALSE)
  if(TARGET YARP::YARP_math)
    set(YARP_HAS_MATH_LIB TRUE)
  endif()
  variable_watch(YARP_HAS_MATH_LIB _yarp_deprecated_variable_warning)

  # YARP_MATH_LIBRARY is deprecated since YARP 3.0.0
  macro(_YARP_HAS_MATH_LIB_IS_DEPRECATED _variable)
    message(DEPRECATION "The ${_variable} variable is deprecated. You can check for YARP_math using find_package(YARP COMPONENTS math)")
  endmacro()
  variable_watch(YARP_MATH_LIBRARY _YARP_HAS_MATH_LIB_IS_DEPRECATED)

  # YARP_VERSION_ABI is deprecated since YARP 3.0.0
  set(YARP_VERSION_ABI "3")
  variable_watch(YARP_VERSION_ABI _yarp_deprecated_variable_warning)

  # YARP_INCLUDE_DIRS is deprecated since YARP 3.0.0
  variable_watch(YARP_INCLUDE_DIRS _yarp_deprecated_variable_warning)

  # YARP_MODULE_PATH is deprecated since YARP 3.0.0
  macro(_YARP_MODULE_PATH_IS_DEPRECATED _variable)
    message(DEPRECATION "The ${_variable} variable is deprecated. CMake find package modules are now in YCM.")
  endmacro()
  set(YARP_MODULE_PATH "${YARP_MODULE_DIR}"
                       "${YARP_MODULE_DIR}/deprecated"
                       ${_YARP_YCM_MODULE_PATH})
  variable_watch(YARP_MODULE_PATH _yarp_module_path_is_deprecated)

  # YARP_DEFINES is deprecated since YARP 3.0.0
  variable_watch(YARP_DEFINES _yarp_deprecated_variable_warning)

  # YARP_HAS_IDL is deprecated since YARP 3.0.0
  variable_watch(YARP_HAS_IDL _yarp_deprecated_variable_warning)

  if(NOT COMMAND yarp_add_idl)
    macro(YARP_ADD_IDL)
      message(DEPRECATION "Calling \"yarp_add_idl\" without including YARP \"idl_tools\" COMPONENT in \"find_package(YARP)\" is deprecated.")
      get_property(_yarp_idl_tools_transitive_dependency_set GLOBAL PROPERTY _CMAKE_YARP_idl_tools_TRANSITIVE_DEPENDENCY SET)
      find_package(YARP_idl_tools
                  ${_YARP_FIND_PARTS_QUIET}
                  ${_YARP_FIND_PART_idl_tools_REQUIRED}
                  HINTS "${YARP_CMAKECONFIG_DIR}"
                  NO_DEFAULT_PATH)
      # Ensure that YARP_idl_tools is not shown by FeatureSummary if not requested
      # by the user
      if(NOT _yarp_idl_tools_transitive_dependency_set)
        set_property(GLOBAL PROPERTY _CMAKE_YARP_idl_tools_TRANSITIVE_DEPENDENCY TRUE)
      endif()
      yarp_add_idl(${ARGN})
    endmacro()
  endif()

  if(NOT COMMAND yarp_idl_to_dir)
    macro(YARP_IDL_TO_DIR)
      message(DEPRECATION "Calling \"yarp_idl_to_dir\" without including YARP \"idl_tools\" COMPONENT in \"find_package(YARP)\" is deprecated.")
      get_property(_yarp_idl_tools_transitive_dependency_set GLOBAL PROPERTY _CMAKE_YARP_idl_tools_TRANSITIVE_DEPENDENCY SET)
      find_package(YARP_idl_tools
                  ${_YARP_FIND_PARTS_QUIET}
                  ${_YARP_FIND_PART_idl_tools_REQUIRED}
                  HINTS "${YARP_CMAKECONFIG_DIR}"
                  NO_DEFAULT_PATH)
      # Ensure that YARP_idl_tools is not shown by FeatureSummary if not requested
      # by the user
      if(NOT _yarp_idl_tools_transitive_dependency_set)
        set_property(GLOBAL PROPERTY _CMAKE_YARP_idl_tools_TRANSITIVE_DEPENDENCY TRUE)
      endif()
      yarp_idl_to_dir(${ARGN})
    endmacro()
  endif()

endif()
