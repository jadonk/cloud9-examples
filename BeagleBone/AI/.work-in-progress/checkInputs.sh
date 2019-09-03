# Run this before changeInputs.js to export everything.

cd /sys/class/gpio

for gpio in 74 75 99 111 114 125 164 177 178 179 195 196 208 209 233 236 237 241
do
    echo -n $gpio " "
    echo $gpio > export
done
echo
