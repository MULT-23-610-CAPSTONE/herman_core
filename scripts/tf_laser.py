#!/usr/bin/env python

import rospy
import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import TransformStamped, Vector3


if __name__ == '__main__':
    rospy.init_node('tf_broadcaster')

    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer)

    tf_broadcaster = tf2_ros.TransformBroadcaster()

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            # Look up the transform from camera_pose_frame to the world frame
            transform_stamped = tf_buffer.lookup_transform('camera_pose_frame', 'camera_pose_frame', rospy.Time(0), rospy.Duration(1.0))
            
            # Get the position of camera_pose_frame in the world frame
            camera_pose_position = transform_stamped.transform.translation
            camera_pose_orientation = transform_stamped.transform.rotation

            
            # Create a new transform from camera_pose_frame to laser
            laser_transform_stamped = TransformStamped()
            laser_transform_stamped.header.stamp = rospy.Time.now()
            laser_transform_stamped.header.frame_id = 'camera_pose_frame'
            laser_transform_stamped.child_frame_id = 'laser'
            laser_transform_stamped.transform.translation = Vector3(camera_pose_position.x, camera_pose_position.y, camera_pose_position.z)
            laser_transform_stamped.transform.rotation = camera_pose_orientation

            # Publish the new transform
            tf_broadcaster.sendTransform(laser_transform_stamped)
        
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            pass
        
        rate.sleep()