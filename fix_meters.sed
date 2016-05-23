# sometimes meters become M:C or M:C| for some reason
# this sed quickly goes in and changes those meters to 6/8 (the most common meter I've encountered in this music)
s/M:C|\{0,1\}/M:6\/8/g
