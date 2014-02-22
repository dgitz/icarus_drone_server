FILE(REMOVE_RECURSE
  "../msg_gen"
  "../src/icarus_drone_server/msg"
  "../msg_gen"
  "CMakeFiles/ROSBUILD_genmsg_cpp"
  "../msg_gen/cpp/include/icarus_drone_server/Num.h"
  "../msg_gen/cpp/include/icarus_drone_server/filter_state.h"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_genmsg_cpp.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
