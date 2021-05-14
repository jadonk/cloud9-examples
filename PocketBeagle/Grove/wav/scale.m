% Lab 6: Sounds Synthesis - Part 4.	Create major scale
% Mark A. Yoder
% 27-Apr-2021
fs = 44100;
dur = 0.5;                % Duration of sound
tt = 0 : 1/fs : dur;
tt = tt';

alpha = 4;

%% Part 3.3 -  Major scale
f0 = 440;
T0 = 1/f0;
xx = [];
names = ["do" "xx" "re" "xx" "me" "fa" "xx" "so" "xx" "la" "xx" "ti" "do+"];
for ss = [0 2 4 5 7 9 11 12]
    filename = names(ss+1) + ".wav";
    ff = f0 * 2^(ss/12);
    note = sin(2*pi*ff*tt) .* exp(-alpha*tt);;
    audiowrite(filename, note, fs);
    xx = [xx; note];
end

soundsc(xx, fs);
