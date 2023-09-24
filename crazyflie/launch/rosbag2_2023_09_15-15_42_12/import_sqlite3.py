from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr

# create reader instance and open for reading
with Reader('.') as reader:
    # topic and msgtype information is available on .connections list
    for connection in reader.connections:
        print(connection.topic, connection.msgtype)

    # iterate over messages
    for connection, timestamp, rawdata in reader.messages():
        print(connection.topic)
        if connection.topic == '/poses':
            msg = deserialize_cdr(rawdata, 'motion_capture_tracking_interfaces/msg/NamedPoseArray')
            print(msg.header.frame_id)