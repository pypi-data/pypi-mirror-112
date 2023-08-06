#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "YARP::YARP_priv_tinyxml" for configuration "Release"
set_property(TARGET YARP::YARP_priv_tinyxml APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::YARP_priv_tinyxml PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libYARP_priv_tinyxml.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::YARP_priv_tinyxml )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::YARP_priv_tinyxml "${_IMPORT_PREFIX}/lib/libYARP_priv_tinyxml.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
