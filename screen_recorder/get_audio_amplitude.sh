# turned out we have audio recorded.
ffprobe -f lavfi -i "amovie=/home/jamesbrown/Videos/test.mkv,astats=metadata=1:reset=1" -show_entries frame=pkt_pts_time:frame_tags=lavfi.astats.Overall.RMS_level -of default=noprint_wrappers=1:nokey=1 -sexagesimal -v error

# check if it is effective on other recordings too.
# working.
# ffprobe -f lavfi -i "amovie=/home/jamesbrown/Videos/cyberpunk_logo.mkv,astats=metadata=1:reset=1" -show_entries frame=pkt_pts_time:frame_tags=lavfi.astats.Overall.RMS_level -of default=noprint_wrappers=1:nokey=1 -sexagesimal -v error
