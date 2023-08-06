#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "YARP::yarp_shmem" for configuration "Release"
set_property(TARGET YARP::yarp_shmem APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::yarp_shmem PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libyarp_shmem.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::yarp_shmem )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::yarp_shmem "${_IMPORT_PREFIX}/lib/libyarp_shmem.a" )

# Import target "YARP::yarp_xmlrpc" for configuration "Release"
set_property(TARGET YARP::yarp_xmlrpc APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::yarp_xmlrpc PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libyarp_xmlrpc.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::yarp_xmlrpc )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::yarp_xmlrpc "${_IMPORT_PREFIX}/lib/libyarp_xmlrpc.a" )

# Import target "YARP::yarp_tcpros" for configuration "Release"
set_property(TARGET YARP::yarp_tcpros APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::yarp_tcpros PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libyarp_tcpros.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::yarp_tcpros )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::yarp_tcpros "${_IMPORT_PREFIX}/lib/libyarp_tcpros.a" )

# Import target "YARP::yarpros" for configuration "Release"
set_property(TARGET YARP::yarpros APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::yarpros PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/yarpros"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::yarpros )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::yarpros "${_IMPORT_PREFIX}/bin/yarpros" )

# Import target "YARP::yarp_bayer" for configuration "Release"
set_property(TARGET YARP::yarp_bayer APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::yarp_bayer PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C;CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libyarp_bayer.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::yarp_bayer )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::yarp_bayer "${_IMPORT_PREFIX}/lib/libyarp_bayer.a" )

# Import target "YARP::yarp_portmonitor" for configuration "Release"
set_property(TARGET YARP::yarp_portmonitor APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::yarp_portmonitor PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libyarp_portmonitor.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::yarp_portmonitor )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::yarp_portmonitor "${_IMPORT_PREFIX}/lib/libyarp_portmonitor.a" )

# Import target "YARP::yarp_unix" for configuration "Release"
set_property(TARGET YARP::yarp_unix APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::yarp_unix PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libyarp_unix.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::yarp_unix )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::yarp_unix "${_IMPORT_PREFIX}/lib/libyarp_unix.a" )

# Import target "YARP::yarpcar" for configuration "Release"
set_property(TARGET YARP::yarpcar APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(YARP::yarpcar PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libyarpcar.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS YARP::yarpcar )
list(APPEND _IMPORT_CHECK_FILES_FOR_YARP::yarpcar "${_IMPORT_PREFIX}/lib/libyarpcar.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
