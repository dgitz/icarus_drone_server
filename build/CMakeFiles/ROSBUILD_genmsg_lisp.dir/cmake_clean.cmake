FILE(REMOVE_RECURSE
  "../msg_gen"
  "../src/icarus_drone_server/msg"
  "../msg_gen"
  "CMakeFiles/ROSBUILD_genmsg_lisp"
  "../msg_gen/lisp/Navdata.lisp"
  "../msg_gen/lisp/_package.lisp"
  "../msg_gen/lisp/_package_Navdata.lisp"
  "../msg_gen/lisp/Num.lisp"
  "../msg_gen/lisp/_package.lisp"
  "../msg_gen/lisp/_package_Num.lisp"
  "../msg_gen/lisp/filter_state.lisp"
  "../msg_gen/lisp/_package.lisp"
  "../msg_gen/lisp/_package_filter_state.lisp"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_genmsg_lisp.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
