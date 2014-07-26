# template for "Stopwatch: The Game"
import simplegui

# define global variables
message = "StopWatch Game"
run=False
time=0
interval=100
x=0
y=0
width=200
height=200

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format_time(t):
    """converts tenths of seconds to A:BC.D"""
    #global message
    D = str( t % 10 )
    A = str (int ( t /10 / 60))
    s = int(t / 10) % 60
    if s<10: BC='0'+str(s)
    else: BC=str(s)

    return A + ":" + BC + "." + D
     
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    global run
    timer.start()
    run=True

def stop_handler():
    global run, time, x, y
    timer.stop()
    if run:
        y += 1
        if time % 10 ==0:
            x += 1
        run=False
            

def reset_handler():
    global run, time, x, y
    time=0
    x=0
    y=0
    run=False
    timer.stop()
    

# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time += 1


# define draw handler
def draw(canvas):
    canvas.draw_text(format_time(time), (width/2-50,height/2),36, "Red")
    canvas.draw_text("x/y = " + str(x) + "/" + str(y), (width-100,20), 20, "Yellow")
    
# create frame
frame=simplegui.create_frame(message, width, height)

# register event handlers
frame.add_button("Start", start_handler, 100);
frame.add_button("Stop",  stop_handler, 100);
frame.add_button("Reset", reset_handler, 100);
frame.set_draw_handler(draw)
timer=simplegui.create_timer(interval, tick)


# start frame
frame.start()


# Please remember to review the grading rubric

