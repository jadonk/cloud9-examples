# From: http://software-dl.ti.com/processor-sdk-linux/esd/docs/latest/linux/Foundational_Components/Kernel/Kernel_Drivers/ADC.html#Continuous%20Mode

cd /sys/bus/iio/devices/iio\:device0/
ls -l buffer
# total 0
# -r--r--r-- 1 root gpio 4096 Jul  7 08:00 data_available
# -rw-rw-r-- 1 root gpio 4096 Jul  7 08:00 enable
# -rw-rw-r-- 1 root gpio 4096 Jul  7 08:00 length
# -rw-rw-r-- 1 root gpio 4096 Jul  7 08:00 watermark

ls -al scan_elements/
cat scan_elements/in_voltage1_type
# le:u12/16>>0

# le represents the endianness, here little endian
# u is the sign of the value returned. It could be either u (for unsigned) or s (for signed)
# 12 is the number of relevant bits of information
# 16 is the actual number of bits used to store the datum
# 0 is the number of right shifts needed.

# Enable A2, P9_37
echo 1 > scan_elements/in_voltage1_en   # P9_40
# echo 1 > scan_elements/in_voltage2_en   # P9_37
# echo 1 > scan_elements/in_voltage5_en   # P9_39
echo 512 > buffer/length

# od -d displlays data as 16 bit values.
TMP=/tmp/capture.all
od -d /dev/iio\:device0 > $TMP
# When capturing two channels the data altername between the two
# Get the even indexed values for on channel and the odd of the other
awk '{for (i=2; i<=NF; i+=2) print $i}' $TMP> /tmp/capture1
awk '{for (i=3; i<=NF; i+=2) print $i}' $TMP> /tmp/capture2

# Enable  capture (in another window)
echo 1 > buffer/enable; sleep 0.1 ; echo 0 > buffer/enable
