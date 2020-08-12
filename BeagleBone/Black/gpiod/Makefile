#
# Programs
#
all:	toggle1 toggle2 get getset

toggle1: toggle1.c
	$(CC) $(LDFLAGS) -lgpiod -o $@ $^

toggle2: toggle2.c
	$(CC) $(LDFLAGS) -lgpiod -o $@ $^

get: get.c
	$(CC) $(LDFLAGS) -lgpiod -o $@ $^

getset: getset.c
	$(CC) $(LDFLAGS) -lgpiod -o $@ $^

#
# Objects
#

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm toggle1 toggle2 get getset
