#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "GazeboYarpSynchronizer::ClockRpc" for configuration "Release"
set_property(TARGET GazeboYarpSynchronizer::ClockRpc APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(GazeboYarpSynchronizer::ClockRpc PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libClockRpc.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS GazeboYarpSynchronizer::ClockRpc )
list(APPEND _IMPORT_CHECK_FILES_FOR_GazeboYarpSynchronizer::ClockRpc "${_IMPORT_PREFIX}/lib/libClockRpc.a" )

# Import target "GazeboYarpSynchronizer::GazeboYarpSynchronizer" for configuration "Release"
set_property(TARGET GazeboYarpSynchronizer::GazeboYarpSynchronizer APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(GazeboYarpSynchronizer::GazeboYarpSynchronizer PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libGazeboYarpSynchronizer.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS GazeboYarpSynchronizer::GazeboYarpSynchronizer )
list(APPEND _IMPORT_CHECK_FILES_FOR_GazeboYarpSynchronizer::GazeboYarpSynchronizer "${_IMPORT_PREFIX}/lib/libGazeboYarpSynchronizer.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
