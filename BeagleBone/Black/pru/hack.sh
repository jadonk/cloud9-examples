# base is of the form: blinkInternalLED.pru0.c
base=blinkInternalLED.pru0.c
# noc is blinkInternalLED.pru0
noc=${base%.*}
# prun is pru0
export PRUN=${noc##*.}
PRUN=${PRUN#pru*}
export TARGET=${base%%.*}

echo base=$base, noc=$noc, PRUN=$PRUN, TARGET=$TARGET

make -f /var/lib/cloud9/common/Makefile 