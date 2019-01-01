Edit /etc/udev/rules.d/10-local.rules
ACTION=="add", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="arm"

rosrun joy joy_node __name:=joy_arm
