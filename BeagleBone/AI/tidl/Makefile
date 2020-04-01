all: classification.tidl.so segmentation.tidl.so

include /var/lib/cloud9/common/Makefile

run:
	ti-mct-heap-check -c
	sudo mjpg_streamer -i "input_opencv.so -r 640x480 -d /dev/$(shell fgrep -v vpe /sys/class/video4linux/video*/name | perl -ne '/\/(video\d+)\/name/ && print $$1') --filter ./classification.tidl.so" -o "output_http.so -p 8090 -w /usr/share/mjpg-streamer/www" 2> /dev/null

clean:
	rm -f classification.tidl.so

