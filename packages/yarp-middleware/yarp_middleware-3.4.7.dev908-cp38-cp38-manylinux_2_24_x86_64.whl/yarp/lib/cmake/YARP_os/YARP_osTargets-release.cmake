#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "YARP::YARP_os" for configuration "Release"
set_property(TARGET YARP::YARP_os APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::YARP_os PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libYARP_os.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::YARP_os )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::YARP_os "${_IMPORT_PREFIX}/lib/libYARP_os.a" )

# Import target "YARP::YARP_init" for configuration "Release"
set_property(TARGET YARP::YARP_init APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::YARP_init PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libYARP_init.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::YARP_init )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::YARP_init "${_IMPORT_PREFIX}/lib/libYARP_init.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
