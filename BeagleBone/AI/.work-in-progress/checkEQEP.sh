# Reads all the eqep positions

cd /sys/devices/platform/44000000.ocp/

for eqep in 4843e000.epwmss 48440000.epwmss 48442000.epwmss
do
    echo $eqep ":" `cat $eqep/*.eqep/position`
done
