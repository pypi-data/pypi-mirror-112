#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "YARP::yarppm" for configuration "Release"
set_property(TARGET YARP::yarppm APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::yarppm PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libyarppm.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::yarppm )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::yarppm "${_IMPORT_PREFIX}/lib/libyarppm.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
