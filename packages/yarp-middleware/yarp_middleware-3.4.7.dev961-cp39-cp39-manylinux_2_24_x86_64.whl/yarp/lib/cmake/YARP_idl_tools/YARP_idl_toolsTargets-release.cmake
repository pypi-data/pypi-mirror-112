#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "YARP::yarpidl_thrift" for configuration "Release"
set_property(TARGET YARP::yarpidl_thrift APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::yarpidl_thrift PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/yarpidl_thrift"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::yarpidl_thrift )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::yarpidl_thrift "${_IMPORT_PREFIX}/bin/yarpidl_thrift" )

# Import target "YARP::yarpidl_rosmsg" for configuration "Release"
set_property(TARGET YARP::yarpidl_rosmsg APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::yarpidl_rosmsg PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/yarpidl_rosmsg"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::yarpidl_rosmsg )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::yarpidl_rosmsg "${_IMPORT_PREFIX}/bin/yarpidl_rosmsg" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
