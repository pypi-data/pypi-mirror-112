#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "YARP::YARP_logger" for configuration "Release"
set_property(TARGET YARP::YARP_logger APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::YARP_logger PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libYARP_logger.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::YARP_logger )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::YARP_logger "${_IMPORT_PREFIX}/lib/libYARP_logger.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
