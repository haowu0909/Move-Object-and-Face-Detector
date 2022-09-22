from motion_dedector import df
import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages")
path = "/Users/wuhao/Desktop/Python - Udemy/App2"

from bokeh.plotting import figure, show, output_file

p = figure(x_axis_type = 'datetime', height = 100, width = 500, 
sizing_mode='scale_width', title = "Motion Graph")
# sizing_mode is the adapted the webpage

p.yaxis.minor_tick_line_color = None
# might need to update the version of library 
p.yaxis[0].ticker.desired_num_ticks = 1

q = p.quad(left = df["Start"], right = df["End"], bottom = 0, top =1, color = "green")

output_file(path + "/Motion.html")
show(p)