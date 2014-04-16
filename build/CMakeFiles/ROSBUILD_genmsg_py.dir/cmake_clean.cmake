FILE(REMOVE_RECURSE
  "../msg_gen"
  "../src/icarus_drone_server/msg"
  "../msg_gen"
  "CMakeFiles/ROSBUILD_genmsg_py"
  "../src/icarus_drone_server/msg/__init__.py"
  "../src/icarus_drone_server/msg/_Navdata.py"
  "../src/icarus_drone_server/msg/_Num.py"
  "../src/icarus_drone_server/msg/_filter_state.py"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_genmsg_py.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
