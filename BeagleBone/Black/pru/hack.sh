# base is of the form: blinkInternalLED.pru0.c
base=blinkInternalLED.pru0
# prun is pru0
export PRUN=${base##*.}
PRUN=${PRUN#pru*}
export TARGET=${base%%.*}

echo base=$base, PRUN=$PRUN, TARGET=$TARGET

make -f /var/lib/cloud9/common/Makefile