all: classification.tidl.so

include /var/lib/cloud9/common/Makefile

run:
	ti-mct-heap-check -c
	mjpg_streamer -i "input_opencv.so -r 640x480 --filter ./classification.tidl.so" -o "output_http.so -p 8090 -w /usr/share/mjpg-streamer/www" 2> /dev/null

clean:
	rm -f classification.tidl.so

