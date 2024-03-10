# see if we can get desktop video & audio

# better not to use capture cards, since they are not stable, with no audio and unable to connect with docker containers.
# https://trac.ffmpeg.org/wiki/Capture/Desktop

# when you see few audio sources listed, you should use another capture method (either ALSA or PulseAudio)
# https://trac.ffmpeg.org/wiki/Capture/ALSA
# https://trac.ffmpeg.org/wiki/Capture/PulseAudio

# but you can use capture cards when it is necessary.
# https://trac.ffmpeg.org/wiki/Capture/Webcam

ffmpeg -video_size 1920x1080 -framerate 25 -f x11grab -i :0.0 -f pulse -ac 2 -i nx_voice_out.monitor -y ~/Videos/test.mkv