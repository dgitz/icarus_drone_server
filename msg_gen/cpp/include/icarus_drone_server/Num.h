/* Auto-generated by genmsg_cpp for file /home/dgitz/fuerte_workspace/sandbox/icarus_drone_server/msg/Num.msg */
#ifndef ICARUS_DRONE_SERVER_MESSAGE_NUM_H
#define ICARUS_DRONE_SERVER_MESSAGE_NUM_H
#include <string>
#include <vector>
#include <map>
#include <ostream>
#include "ros/serialization.h"
#include "ros/builtin_message_traits.h"
#include "ros/message_operations.h"
#include "ros/time.h"

#include "ros/macros.h"

#include "ros/assert.h"


namespace icarus_drone_server
{
template <class ContainerAllocator>
struct Num_ {
  typedef Num_<ContainerAllocator> Type;

  Num_()
  : num(0)
  {
  }

  Num_(const ContainerAllocator& _alloc)
  : num(0)
  {
  }

  typedef int64_t _num_type;
  int64_t num;


  typedef boost::shared_ptr< ::icarus_drone_server::Num_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::icarus_drone_server::Num_<ContainerAllocator>  const> ConstPtr;
  boost::shared_ptr<std::map<std::string, std::string> > __connection_header;
}; // struct Num
typedef  ::icarus_drone_server::Num_<std::allocator<void> > Num;

typedef boost::shared_ptr< ::icarus_drone_server::Num> NumPtr;
typedef boost::shared_ptr< ::icarus_drone_server::Num const> NumConstPtr;


template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const  ::icarus_drone_server::Num_<ContainerAllocator> & v)
{
  ros::message_operations::Printer< ::icarus_drone_server::Num_<ContainerAllocator> >::stream(s, "", v);
  return s;}

} // namespace icarus_drone_server

namespace ros
{
namespace message_traits
{
template<class ContainerAllocator> struct IsMessage< ::icarus_drone_server::Num_<ContainerAllocator> > : public TrueType {};
template<class ContainerAllocator> struct IsMessage< ::icarus_drone_server::Num_<ContainerAllocator>  const> : public TrueType {};
template<class ContainerAllocator>
struct MD5Sum< ::icarus_drone_server::Num_<ContainerAllocator> > {
  static const char* value() 
  {
    return "57d3c40ec3ac3754af76a83e6e73127a";
  }

  static const char* value(const  ::icarus_drone_server::Num_<ContainerAllocator> &) { return value(); } 
  static const uint64_t static_value1 = 0x57d3c40ec3ac3754ULL;
  static const uint64_t static_value2 = 0xaf76a83e6e73127aULL;
};

template<class ContainerAllocator>
struct DataType< ::icarus_drone_server::Num_<ContainerAllocator> > {
  static const char* value() 
  {
    return "icarus_drone_server/Num";
  }

  static const char* value(const  ::icarus_drone_server::Num_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator>
struct Definition< ::icarus_drone_server::Num_<ContainerAllocator> > {
  static const char* value() 
  {
    return "int64 num\n\
\n\
";
  }

  static const char* value(const  ::icarus_drone_server::Num_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator> struct IsFixedSize< ::icarus_drone_server::Num_<ContainerAllocator> > : public TrueType {};
} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

template<class ContainerAllocator> struct Serializer< ::icarus_drone_server::Num_<ContainerAllocator> >
{
  template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
  {
    stream.next(m.num);
  }

  ROS_DECLARE_ALLINONE_SERIALIZER;
}; // struct Num_
} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::icarus_drone_server::Num_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const  ::icarus_drone_server::Num_<ContainerAllocator> & v) 
  {
    s << indent << "num: ";
    Printer<int64_t>::stream(s, indent + "  ", v.num);
  }
};


} // namespace message_operations
} // namespace ros

#endif // ICARUS_DRONE_SERVER_MESSAGE_NUM_H
