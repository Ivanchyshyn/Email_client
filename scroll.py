from tkinter import Canvas, Frame, ttk, VERTICAL, N, W, E, S
def scroll_bar(mainframe):
    scroll = ttk.Scrollbar(mainframe, orient=VERTICAL)
    canvas = Canvas(mainframe, scrollregion=(0, 0, 1000, 1200), yscrollcommand=scroll.set)
    scroll['command'] = canvas.yview

    frame = Frame(canvas)
    frame_id = canvas.create_window((0, 0), window=frame, anchor='nw')
    ttk.Sizegrip(mainframe).grid(column=2, row=1, sticky=(S, E))

    canvas.grid(column=0, row=0, sticky=(N, W, E, S))
    scroll.grid(column=2, row=0, sticky=(N, S))

    # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar
    def _configure_frame(event):
        # update the scrollbars to match the size of the inner frame
        size = (frame.winfo_reqwidth(), frame.winfo_reqheight())
        canvas.config(scrollregion="0 0 %s %s" % size)
        if frame.winfo_reqwidth() != canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            canvas.config(width=frame.winfo_reqwidth())
        del event
    frame.bind('<Configure>', _configure_frame)

    def _configure_canvas(event):
        if frame.winfo_reqwidth() != canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            canvas.itemconfigure(frame_id, width=canvas.winfo_width())
        del event
    canvas.bind('<Configure>', _configure_canvas)
    return frame
