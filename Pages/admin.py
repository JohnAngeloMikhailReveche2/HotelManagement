import tkinter as tk
from email.policy import default
from tkinter import messagebox as mb, StringVar
from tkinter import ttk
import tkinter.font as tkFont
from tkcalendar import DateEntry









# Color HEX Constants
# https://www.color-hex.com/color-palette/1061596
TOP_FRAME_COLOR = "#1a3f73"
DASHBOARD_FRAME_COLOR = "#598dba"
DASHBOARD_BUTTON_COLOR = "#4d6b88"
LOGOUT_BUTTON_COLOR = "#407099"

# CONSTANTS
COLUMN_WIDTH = 100


# METHODS
def centerScreen():
    # Screen Dimension
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()

    # Calculate the Center Point
    centerX = int(screenWidth / 2 - windowWidth / 2)
    centerY = int(screenHeight / 2 - windowHeight / 2)

    # Set the geometry based on the Window and Screen Calculations
    root.geometry(f"{windowWidth}x{windowHeight}+{centerX}+{centerY}")




def modelTopFrame():

    topFrame = tk.Frame(canvas
                        , bg=TOP_FRAME_COLOR
                        , height=85
                        , width=windowWidth
                        )
    topFrame.pack_propagate(False)

    lblTitle = tk.Label(topFrame
                        , text="Hotel Management"
                        , fg="white"
                        , bg=TOP_FRAME_COLOR
                        , font=tkFont.Font(family="Arial"
                                           , size=21
                                           , weight="bold"
                                           )
                        )
    lblTitle.pack(pady=(20, 0)
                  , padx=(15, 0)
                  , anchor="w"
                  )

    return topFrame

def modelDashboardFrame():

    def onRoomStatusClick():
        AD_ROOMSTAT_FRAME.lift()
        btnRoomStatus.config(bg="white"
                         , fg=DASHBOARD_BUTTON_COLOR
                         )
        btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="white"
                             )
        btnIDCreate.config(bg=DASHBOARD_FRAME_COLOR
                           , fg="white"
                           )
        btnRoomCreate.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="white"
                             )

    def onHistoryClick():
        AD_HISTORY_FRAME.lift()
        btnHistory.config(bg="white"
                         , fg=DASHBOARD_BUTTON_COLOR
                         )
        btnRoomStatus.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="white"
                             )
        btnIDCreate.config(bg=DASHBOARD_FRAME_COLOR
                           , fg="white"
                           )
        btnRoomCreate.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="white"
                             )
        btnPricing.config(bg=DASHBOARD_FRAME_COLOR
                          , fg="white"
                          )

    def onIDCreateClick():
        AD_IDCREATE_FRAME.lift()
        btnIDCreate.config(bg="white"
                         , fg=DASHBOARD_BUTTON_COLOR
                         )
        btnRoomStatus.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="white"
                             )
        btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                          , fg="white"
                          )
        btnRoomCreate.config(bg=DASHBOARD_FRAME_COLOR
                           , fg="white"
                           )
        btnPricing.config(bg=DASHBOARD_FRAME_COLOR
                          , fg="white"
                          )

    def onRoomCreateClick():
        AD_ROOMCREATE_FRAME.lift()
        btnRoomCreate.config(bg="white"
                         , fg=DASHBOARD_BUTTON_COLOR
                         )
        btnRoomStatus.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="white"
                             )
        btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                          , fg="white"
                          )
        btnIDCreate.config(bg=DASHBOARD_FRAME_COLOR
                           , fg="white"
                           )
        btnPricing.config(bg=DASHBOARD_FRAME_COLOR
                           , fg="white"
                           )

    def onPricingClick():
        AD_PRICING_FRAME.lift()
        btnPricing.config(bg="white"
                         , fg=DASHBOARD_BUTTON_COLOR
                         )
        btnRoomStatus.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="white"
                             )
        btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                          , fg="white"
                          )
        btnIDCreate.config(bg=DASHBOARD_FRAME_COLOR
                           , fg="white"
                           )
        btnRoomCreate.config(bg=DASHBOARD_FRAME_COLOR
                           , fg="white"
                           )

    # Button Initialization
    dashboardFrame = tk.Frame(canvas
                        , bg=DASHBOARD_FRAME_COLOR
                        , height=windowHeight
                        , width=230
                        )
    dashboardFrame.pack_propagate(False)

    buttonFrame = tk.Frame(dashboardFrame
                              , bg="white"
                              , height=50
                              , width=230
                              )
    buttonFrame.pack_propagate(False)
    buttonFrame.pack( pady = (150, 0)
                      )

    btnRoomStatus = tk.Button(buttonFrame
                        , text= "Room Status"
                        , fg= DASHBOARD_BUTTON_COLOR
                        , bg= "white"
                        , height = 50
                        , width = 230
                        , borderwidth= 0
                        , highlightthickness= 0
                        , activebackground= "white"
                        , activeforeground= DASHBOARD_BUTTON_COLOR
                        , relief = tk.FLAT
                        , font=tkFont.Font(family="Arial"
                                           , size=12
                                           , weight="bold"
                                           )
                        , command = onRoomStatusClick
                        )
    btnRoomStatus.pack( anchor="n" )

    buttonFrame2 = tk.Frame(dashboardFrame
                           , bg=DASHBOARD_FRAME_COLOR
                           , height=50
                           , width=230
                           )
    buttonFrame2.pack_propagate(False)
    buttonFrame2.pack(pady=(20, 0)
                     )

    btnHistory = tk.Button(buttonFrame2
                           , text="History"
                           , fg="white"
                           , bg=DASHBOARD_FRAME_COLOR
                           , height=50
                           , width=230
                           , borderwidth=0
                           , highlightthickness=0
                           , activebackground="white"
                           , activeforeground=DASHBOARD_BUTTON_COLOR
                           , relief=tk.FLAT
                           , font=tkFont.Font(family="Arial"
                                              , size=12
                                              , weight="bold"
                                              )
                           , command = onHistoryClick
                           )
    btnHistory.pack(anchor="n")

    buttonFrame3 = tk.Frame(dashboardFrame
                            , bg=DASHBOARD_FRAME_COLOR
                            , height=50
                            , width=230
                            )
    buttonFrame3.pack_propagate(False)
    buttonFrame3.pack(pady=(20, 0)
                      )

    btnIDCreate = tk.Button(buttonFrame3
                          , text="I.D Proof Creation"
                          , fg="white"
                          , bg=DASHBOARD_FRAME_COLOR
                          , height=50
                          , width=230
                          , borderwidth=0
                          , highlightthickness=0
                          , activebackground="white"
                          , activeforeground=DASHBOARD_BUTTON_COLOR
                          , relief=tk.FLAT
                          , font=tkFont.Font(family="Arial"
                                             , size=12
                                             , weight="bold"
                                             )
                          , command = onIDCreateClick
                          )
    btnIDCreate.pack(anchor="n")

    buttonFrame4 = tk.Frame(dashboardFrame
                            , bg=DASHBOARD_FRAME_COLOR
                            , height=50
                            , width=230
                            )
    buttonFrame4.pack_propagate(False)
    buttonFrame4.pack(pady=(20, 0)
                      )

    btnRoomCreate = tk.Button(buttonFrame4
                           , text="Room Creation"
                           , fg="white"
                           , bg=DASHBOARD_FRAME_COLOR
                           , height=50
                           , width=230
                           , borderwidth=0
                           , highlightthickness=0
                           , activebackground="white"
                           , activeforeground=DASHBOARD_BUTTON_COLOR
                           , relief=tk.FLAT
                           , font=tkFont.Font(family="Arial"
                                              , size=12
                                              , weight="bold"
                                              )
                           , command = onRoomCreateClick
                           )
    btnRoomCreate.pack(anchor="n")

    buttonFrame7 = tk.Frame(dashboardFrame
                            , bg=DASHBOARD_FRAME_COLOR
                            , height=50
                            , width=230
                            )
    buttonFrame7.pack_propagate(False)
    buttonFrame7.pack(pady=(20, 0)
                      )

    btnPricing = tk.Button(buttonFrame7
                            , text="Check Hours"
                            , fg="white"
                            , bg=DASHBOARD_FRAME_COLOR
                            , height=50
                            , width=230
                            , borderwidth=0
                            , highlightthickness=0
                            , activebackground="white"
                            , activeforeground=DASHBOARD_BUTTON_COLOR
                            , relief=tk.FLAT
                            , font=tkFont.Font(family="Arial"
                                               , size=12
                                               , weight="bold"
                                               )
                            , command = onPricingClick
                            )
    btnPricing.pack(anchor="n")

    buttonFrame5 = tk.Frame(dashboardFrame
                            , bg=DASHBOARD_FRAME_COLOR
                            , height=50
                            , width=230
                            )
    buttonFrame5.pack_propagate(False)
    buttonFrame5.pack(pady=(190, 0)
                      , anchor="n"
                      )

    btnLogOut = tk.Button(buttonFrame5
                            , text="Log Out"
                            , fg="white"
                            , bg=LOGOUT_BUTTON_COLOR
                            , height=50
                            , width=230
                            , borderwidth=0
                            , highlightthickness=0
                            , activebackground="white"
                            , activeforeground=DASHBOARD_BUTTON_COLOR
                            , relief=tk.FLAT
                            , font=tkFont.Font(family="Arial"
                                               , size=12
                                               , weight="bold"
                                               )
                            )
    btnLogOut.pack(anchor="n")

    return dashboardFrame

def modelRoomStatus():
    # Note:
    # Scroll_Canvas - is the scrollable area, the actual Canvas widget that can scroll.
    # mainBookingFrame - The contents placed in the canvas, holding widgets. It doesn't scroll itself
    #                     it is moved around by canvas.

    # Main Whole Frame
    frame = tk.Frame(canvas
                     , bg="white"
                     , height=635
                     , width=1050
                     )
    # This forces the frame to keep the fixed size regardless what's inside of it.
    frame.pack_propagate(False)

    # A scrollable canvas embedded in the bookingFrame and a scrollbar
    scroll_canvas = tk.Canvas(frame, width=1050, bg="white")
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=scroll_canvas.yview)

    # Linking the canvas to the scrollbar so
    # when the canvas moves the scrollbar's thumb pos will also move.
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    # expand=True means the canvas will grow as the BookingFrame grows.
    scroll_canvas.pack(side="left", fill="both", expand=True)

    # This frame contains the actual scrollable contents
    mainFrame = tk.Frame(scroll_canvas, bg="white")
    # Embedding the mainBookingFrame to the scroll canvas
    scroll_canvas.create_window((0, 0), window=mainFrame, anchor="nw")

    # Events

    # This allows the canvas to know that the scrollable area has a specified tall
    # so that it can be updated or be scrolled
    def update_scrollregion(e):
        canvas_height = scroll_canvas.winfo_height()
        content_bbox = scroll_canvas.bbox("all")

        if content_bbox:
            content_height = content_bbox[3] - content_bbox[1]  # bottom - top

            # Only set scrollregion if content is taller than the canvas
            if content_height > canvas_height:
                scroll_canvas.configure(scrollregion=content_bbox)
            else:
                # Lock scrolling — set scrollregion to visible canvas only
                scroll_canvas.configure(scrollregion=(0, 0, 0, canvas_height))

    # Whenever the frame changes size,
    # it Recalculates the scroll region when the mainBookingFrame size changes
    mainFrame.bind("<Configure>", update_scrollregion)

    def on_mousewheel(e):
        content_bbox = scroll_canvas.bbox("all")
        if content_bbox:
            content_height = content_bbox[3] - content_bbox[1]
            canvas_height = scroll_canvas.winfo_height()

            if content_height > canvas_height:
                scroll_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

    scroll_canvas.bind("<Enter>", lambda e: scroll_canvas.bind_all("<MouseWheel>", on_mousewheel))
    scroll_canvas.bind("<Leave>", lambda e: scroll_canvas.unbind_all("<MouseWheel>"))

    # Main UI Elements inside

    lblTitle = tk.Label(mainFrame
                        , text="Room Status"
                        , fg="black"
                        , bg="white"
                        , font=tkFont.Font(family="Arial"
                                           , size=21
                                           , weight="bold"
                                           )
                        )
    lblTitle.pack(pady=(20, 0)
                  , padx=(20, 0)
                  , anchor="w"
                  )

    btnFrame = tk.Frame(mainFrame
                        , bg="white"
                        )
    btnFrame.pack(anchor="w")

    lblSearchBy = tk.Label(btnFrame
                           , text="Search By"
                           , fg="black"
                           , bg="white"
                           , font=tkFont.Font(family="Arial"
                                              , size=12
                                              , weight="bold"
                                              )
                           )
    lblSearchBy.pack(pady=(24, 0)
                     , padx=(10, 0)
                     , anchor="w"
                     , side="left"
                     )

    selectedFilter = StringVar()
    filterCmb = ttk.Combobox(btnFrame
                             , textvariable=selectedFilter
                             , state="readonly"
                             , width=20
                             )
    filterCmb['values'] = ('All'
                           , 'Room Type'
                           , 'Bed Type'
                           , 'Status'
                           )
    filterCmb.pack(pady=(25, 0), padx=(10, 0), side="left", anchor="w")
    filterCmb.current(0)

    searchEntry = tk.Entry(btnFrame
                           , width=30
                           , borderwidth=3
                           )
    searchEntry.pack(pady=(25, 0), padx=(10, 0), side="left", anchor="w")

    btnSearch = tk.Button(btnFrame
                          , text="Search"
                          , pady=5
                          , padx=40
                          )
    btnSearch.pack(pady=(20, 0), padx=(15, 0), side="left", anchor="w")

    btnReset = tk.Button(btnFrame
                         , text="Reset"
                         , pady=5
                         , padx=40
                         )
    btnReset.pack(pady=(20, 0), padx=(20, 0), side="left", anchor="w")

    treeContainer = tk.Frame(mainFrame
                             , width=1000
                             , height=400
                             , bg="white"
                             )
    treeContainer.pack(padx=10, pady=10)
    treeContainer.pack_propagate(False)

    # Treeview Widget
    roomTree = ttk.Treeview(treeContainer, show="headings", height=17)

    # Columns
    roomTree['columns'] = ("Room Number"
                           , "Room Type"
                           , "Bed Type"
                           , "Status"
                           )

    # Formatting Columns
    roomTree.column("Room Number"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
    roomTree.column("Room Type"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
    roomTree.column("Bed Type"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
    roomTree.column("Status"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )

    # Headings
    roomTree.heading("Room Type", text="Room Type")
    roomTree.heading("Bed Type", text="Bed Type")
    roomTree.heading("Room Number", text="Room Number")
    roomTree.heading("Status", text="Status")

    # Horizontal Scrollbar
    scrollbar = ttk.Scrollbar(treeContainer
                              , orient="horizontal"
                              , command=roomTree.xview
                              )
    roomTree.configure(xscrollcommand=scrollbar.set)

    # Pack
    roomTree.pack(pady=(10, 0), padx=(10, 0), anchor="nw")
    scrollbar.pack(side="bottom", fill="x")

    return frame

def modelHistoryFrame():

    # Note:
    # Scroll_Canvas - is the scrollable area, the actual Canvas widget that can scroll.
    # mainBookingFrame - The contents placed in the canvas, holding widgets. It doesn't scroll itself
    #                     it is moved around by canvas.

    # Main Whole Frame
    frame = tk.Frame(canvas
                              , bg="white"
                              , height=635
                              , width=1050
                              )
    # This forces the frame to keep the fixed size regardless what's inside of it.
    frame.pack_propagate(False)

    # A scrollable canvas embedded in the bookingFrame and a scrollbar
    scroll_canvas = tk.Canvas(frame, width = 1050, bg="white")
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=scroll_canvas.yview)

    # Linking the canvas to the scrollbar so
    # when the canvas moves the scrollbar's thumb pos will also move.
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    # expand=True means the canvas will grow as the BookingFrame grows.
    scroll_canvas.pack(side="left", fill="both", expand=True)

    # This frame contains the actual scrollable contents
    mainFrame = tk.Frame(scroll_canvas, bg="white")
    # Embedding the mainBookingFrame to the scroll canvas
    scroll_canvas.create_window((0,0), window=mainFrame, anchor="nw")


    # Events

    # This allows the canvas to know that the scrollable area has a specified tall
    # so that it can be updated or be scrolled
    def update_scrollregion(e):
        canvas_height = scroll_canvas.winfo_height()
        content_bbox = scroll_canvas.bbox("all")

        if content_bbox:
            content_height = content_bbox[3] - content_bbox[1]  # bottom - top

            # Only set scrollregion if content is taller than the canvas
            if content_height > canvas_height:
                scroll_canvas.configure(scrollregion=content_bbox)
            else:
                # Lock scrolling — set scrollregion to visible canvas only
                scroll_canvas.configure(scrollregion=(0, 0, 0, canvas_height))
    # Whenever the frame changes size,
    # it Recalculates the scroll region when the mainBookingFrame size changes
    mainFrame.bind("<Configure>", update_scrollregion)

    def on_mousewheel(e):
        content_bbox = scroll_canvas.bbox("all")
        if content_bbox:
            content_height = content_bbox[3] - content_bbox[1]
            canvas_height = scroll_canvas.winfo_height()

            if content_height > canvas_height:
                scroll_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
    scroll_canvas.bind("<Enter>", lambda e: scroll_canvas.bind_all("<MouseWheel>", on_mousewheel))
    scroll_canvas.bind("<Leave>", lambda e: scroll_canvas.unbind_all("<MouseWheel>"))


    # Main UI Elements inside

    lblTitle = tk.Label(mainFrame
                        , text="History"
                        , fg="black"
                        , bg="white"
                        , font=tkFont.Font(family="Arial"
                                           , size=21
                                           , weight="bold"
                                           )
                        )
    lblTitle.pack(pady=(20, 0)
                  , padx=(20, 0)
                  , anchor="w"
                  )

    btnFrame = tk.Frame(mainFrame
                        , bg="white"
                     )
    btnFrame.pack(anchor="w")

    lblSearchBy = tk.Label(btnFrame
                        , text="Search By"
                        , fg="black"
                        , bg="white"
                        , font=tkFont.Font(family="Arial"
                                           , size=12
                                           , weight="bold"
                                           )
                        )
    lblSearchBy.pack(pady=(24, 0)
                  , padx=(10, 0)
                  , anchor="w"
                  , side="left"
                  )

    selectedFilter = StringVar()
    filterCmb = ttk.Combobox(btnFrame
                             , textvariable=selectedFilter
                             , state="readonly"
                             , width=20
                             )
    filterCmb['values'] = ('All'
                           , 'Name'
                           , 'Contact'
                           , 'ID Proof'
                           , 'Room Type'
                           , 'Bed Type'
                           , 'Room Number'
                           , 'Check-In'
                           , 'Check-Out'
                           , 'Rent Time'
                           )
    filterCmb.pack(pady=(25, 0), padx=(10, 0), side="left", anchor="w")
    filterCmb.current(0)

    searchEntry = tk.Entry(btnFrame
                           , width=30
                           , borderwidth=3
                           )
    searchEntry.pack(pady=(25,0), padx=(10,0), side="left", anchor="w")

    btnSearch = tk.Button(btnFrame
                          , text="Search"
                          , pady=5
                          , padx=40
                          )
    btnSearch.pack(pady=(20, 0), padx=(15, 0), side="left", anchor="w")

    btnReset = tk.Button(btnFrame
                          , text="Reset"
                          , pady=5
                          , padx=40
                          )
    btnReset.pack(pady=(20, 0), padx=(20, 0), side="left", anchor="w")




    treeContainer = tk.Frame(mainFrame
                             , width=1000
                             , height=400
                             , bg="white"
                             )
    treeContainer.pack(padx=10, pady=10)
    treeContainer.pack_propagate(False)

    # Treeview Widget
    tree = ttk.Treeview(treeContainer, show="headings", height=17)

    # Columns
    tree['columns'] = ("Name"
                       , "Contact"
                       , "Address"
                       , "ID Proof"
                       , "Room Type"
                       , "Bed Type"
                       , "Room Number"
                       , "Check-In"
                       , "Check-Out"
                       , "Rent Time"
                       , "Total Price"
                       )

    # Formatting Columns
    tree.column("Name"
                , anchor=tk.W
                , width=COLUMN_WIDTH
                )
    tree.column("Contact"
                , anchor=tk.W
                , width=COLUMN_WIDTH
                )
    tree.column("Address"
                , anchor=tk.W
                , width=COLUMN_WIDTH
                )
    tree.column("ID Proof"
                , anchor=tk.W
                , width=COLUMN_WIDTH
                )
    tree.column("Room Type"
                , anchor=tk.W
                , width=COLUMN_WIDTH
                )
    tree.column("Bed Type"
                , anchor=tk.W
                , width=COLUMN_WIDTH
                )
    tree.column("Room Number"
                , anchor=tk.W
                , width=COLUMN_WIDTH
                )
    tree.column("Check-In"
                , anchor=tk.W
                , width=COLUMN_WIDTH
                )
    tree.column("Check-Out"
                , anchor=tk.W
                , width=COLUMN_WIDTH
                )
    tree.column("Rent Time"
                , anchor=tk.W
                , width=COLUMN_WIDTH
                )
    tree.column("Total Price"
                , anchor=tk.W
                , width=COLUMN_WIDTH
                )

    # Create Headings
    tree.heading("Name"
                 , text="Name"
                 , anchor=tk.W
                 )
    tree.heading("Contact"
                 , text="Contact"
                 , anchor=tk.W
                 )
    tree.heading("Address"
                 , text="Address"
                 , anchor=tk.W
                 )
    tree.heading("ID Proof"
                 , text="ID Proof"
                 , anchor=tk.W
                 )
    tree.heading("Room Type"
                 , text="Room Type"
                 , anchor=tk.W
                 )
    tree.heading("Bed Type"
                 , text="Bed Type"
                 , anchor=tk.W
                 )
    tree.heading("Room Number"
                 , text="Room Number"
                 , anchor=tk.W
                 )
    tree.heading("Check-In"
                 , text="Check-In"
                 , anchor=tk.W
                 )
    tree.heading("Check-Out"
                 , text="Check-Out"
                 , anchor=tk.W
                 )
    tree.heading("Rent Time"
                 , text="Rent Time"
                 , anchor=tk.W
                 )
    tree.heading("Total Price"
                 , text="Total Price"
                 , anchor=tk.W
                 )

    # Horizontal Scrollbar
    scrollbar = ttk.Scrollbar(treeContainer
                              , orient="horizontal"
                              , command=tree.xview
                              )
    tree.configure(xscrollcommand=scrollbar.set)

    # Pack
    tree.pack(pady=(10,0), padx=(10,0), anchor="nw")
    scrollbar.pack(side="bottom", fill="x")

    return frame

def modelIDCreate():

    # Main Whole Frame
    frame = tk.Frame(canvas
                              , bg="white"
                              , height=635
                              , width=1050
                              )
    # This forces the frame to keep the fixed size regardless what's inside of it.
    frame.pack_propagate(False)


    # Main UI Elements inside

    lblTitle = tk.Label(frame
                        , text="I.D Creation"
                        , fg="black"
                        , bg="white"
                        , font=tkFont.Font(family="Arial"
                                           , size=21
                                           , weight="bold"
                                           )
                        )
    lblTitle.pack(pady=(20, 0)
                  , padx=(20, 0)
                  , anchor="w"
                  )

    btnFrame = tk.Frame(frame
                        , bg="white"
                     )
    btnFrame.pack(anchor="n")

    dataEntry = tk.Entry(btnFrame
                           , width=30
                           , borderwidth=3
                           )
    dataEntry.pack(pady=(25, 0), padx=(10, 0), side="left", anchor="w")

    btnAdd = tk.Button(btnFrame
                          , text="Add"
                          , pady=5
                          , padx=40
                          )
    btnAdd.pack(pady=(20, 0), padx=(15, 0), side="left", anchor="w")

    btnUpdate = tk.Button(btnFrame
                          , text="Update"
                          , pady=5
                          , padx=40
                          )
    btnUpdate.pack(pady=(20, 0), padx=(20, 0), side="left", anchor="w")

    btnDelete = tk.Button(btnFrame
                          , text="Delete"
                          , pady=5
                          , padx=40
                          )
    btnDelete.pack(pady=(20, 0), padx=(20, 0), side="left", anchor="w")




    treeContainer = tk.Frame(frame
                             , width=1000
                             , height=400
                             , bg="white"
                             )
    treeContainer.pack(padx=10, pady=10)
    treeContainer.pack_propagate(False)

    # Treeview Widget
    tree = ttk.Treeview(treeContainer, show="headings", height=17)

    # Columns
    tree['columns'] = ("IDType"
                       )

    # Formatting Columns
    tree.column("IDType"
                , anchor=tk.W
                , width=600
                )

    # Create Headings
    tree.heading("IDType"
                 , text="ID Type"
                 , anchor=tk.W
                 )

    # Pack
    tree.pack(pady=(10,0), padx=(10,0), anchor="n")

    return frame

def modelRoomCreate():

    # Note:
    # Scroll_Canvas - is the scrollable area, the actual Canvas widget that can scroll.
    # mainBookingFrame - The contents placed in the canvas, holding widgets. It doesn't scroll itself
    #                     it is moved around by canvas.

    # Main Whole Frame
    frame = tk.Frame(canvas
                              , bg="white"
                              , height=635
                              , width=1050
                              )
    # This forces the frame to keep the fixed size regardless what's inside of it.
    frame.pack_propagate(False)

    # A scrollable canvas embedded in the bookingFrame and a scrollbar
    scroll_canvas = tk.Canvas(frame, width = 1050, bg="white")
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=scroll_canvas.yview)

    # Linking the canvas to the scrollbar so
    # when the canvas moves the scrollbar's thumb pos will also move.
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    # expand=True means the canvas will grow as the BookingFrame grows.
    scroll_canvas.pack(side="left", fill="both", expand=True)

    # This frame contains the actual scrollable contents
    mainBookingFrame = tk.Frame(scroll_canvas, bg="white")
    # Embedding the mainBookingFrame to the scroll canvas
    scroll_canvas.create_window((0,0), window=mainBookingFrame, anchor="nw")


    # Events

    # This allows the canvas to know that the scrollable area has a specified tall
    # so that it can be updated or be scrolled
    def update_scrollregion(e):
        canvas_height = scroll_canvas.winfo_height()
        content_bbox = scroll_canvas.bbox("all")

        if content_bbox:
            content_height = content_bbox[3] - content_bbox[1]  # bottom - top

            # Only set scrollregion if content is taller than the canvas
            if content_height > canvas_height:
                scroll_canvas.configure(scrollregion=content_bbox)
            else:
                # Lock scrolling — set scrollregion to visible canvas only
                scroll_canvas.configure(scrollregion=(0, 0, 0, canvas_height))
    # Whenever the frame changes size,
    # it Recalculates the scroll region when the mainBookingFrame size changes
    mainBookingFrame.bind("<Configure>", update_scrollregion)

    def on_mousewheel(e):
        content_bbox = scroll_canvas.bbox("all")
        if content_bbox:
            content_height = content_bbox[3] - content_bbox[1]
            canvas_height = scroll_canvas.winfo_height()

            if content_height > canvas_height:
                scroll_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
    scroll_canvas.bind("<Enter>", lambda e: scroll_canvas.bind_all("<MouseWheel>", on_mousewheel))
    scroll_canvas.bind("<Leave>", lambda e: scroll_canvas.unbind_all("<MouseWheel>"))


    # Main UI Elements inside

    lblTitle = tk.Label(mainBookingFrame
                        , text="Create A Room"
                        , fg="black"
                        , bg="white"
                        , font=tkFont.Font(family="Arial"
                                           , size=21
                                           , weight="bold"
                                           )
                        )
    lblTitle.pack(pady=(20, 0)
                  , padx=(20, 0)
                  , anchor="w"
                  )

    # ======================= ROOM TYPE INFO ===============================

    roomTypeInfo = tk.LabelFrame(mainBookingFrame
                             , text="Room Type Creation"
                             , padx=20
                             , pady=20
                             , bg="white"
                             , font=tkFont.Font(family="Arial"
                                                , size=12
                                                , weight="bold"
                                                )
                             )
    roomTypeInfo.pack(padx=20
                  , pady=20
                  , anchor = "nw"
                  )

    rType = tk.Label(roomTypeInfo
                     , text="Room Type:"
                     , bg="white"
                     , anchor="w"
                     )
    rType.grid(row=0, column=1, padx=(0, 10))
    rTypeEntry = tk.Entry(roomTypeInfo
                          , bg="white"
                          , width=25
                          )
    rTypeEntry.grid(row=0, column=2)

    btnCreate = tk.Button(roomTypeInfo
                          , text="Create"
                          , width=20
                          , pady=10
                          )
    btnCreate.grid(row=1, column=2, pady=(20, 0))

    btnUpdate = tk.Button(roomTypeInfo
                          , text="Update"
                          , width=20
                          , pady=10
                          )
    btnUpdate.grid(row=1, column=4, pady=(20, 0), padx=(20, 0))

    btnDelete = tk.Button(roomTypeInfo
                          , text="Delete"
                          , width=20
                          , pady=10
                          )
    btnDelete.grid(row=1, column=6, pady=(20, 0), padx=(20, 0))










    treeContainer = tk.Frame(mainBookingFrame
                             , width=1000
                             , height=400
                             , bg="white"
                             )
    treeContainer.pack(padx=(13, 0), pady=5)
    treeContainer.pack_propagate(False)

    # Treeview Widget
    tree = ttk.Treeview(treeContainer, show="headings", height=17)

    # Columns
    tree['columns'] = ("RoomType"
                       )

    # Formatting Columns
    tree.column("RoomType"
                , anchor=tk.W
                , width=650
                )

    # Create Headings
    tree.heading("RoomType"
                 , text="Room Type"
                 , anchor=tk.W
                 )

    # Pack
    tree.pack(pady=(5, 0), padx=(10, 0), anchor="nw")

    # ======================= ROOM INFO ===============================

    roomInfo = tk.LabelFrame(mainBookingFrame
                                         , text = "Room Creation"
                                         , padx = 20
                                         , pady = 20
                                         , bg = "white"
                                         , font = tkFont.Font(family="Arial"
                                                               , size=12
                                                               , weight="bold"
                                                             )
                                         )
    roomInfo.pack( padx = 20
                  , pady = 20
                  , anchor = "nw"
                    )

    rNumber = tk.Label(roomInfo
                      , text = "Room Number:"
                      , bg = "white"
                      , anchor = "w"
                      )
    rNumber.grid(row=0, column=1, padx=(0, 10))
    rNumberEntry = tk.Entry(roomInfo
                     , bg = "white"
                     , width = 25
                     )
    rNumberEntry.grid(row=0, column=2)

    rTypeSelect = tk.Label(roomInfo
                     , text="Room Type:"
                     , bg="white"
                     )
    rTypeSelect.grid(row=0, column=3, padx=(20,10))
    rTypeCombo = ttk.Combobox(roomInfo,
                         values=["Single", "Double", "Family"],
                         state="readonly",
                         font=("Arial", 10),
                         width=25
                              )
    rTypeCombo.grid(row=0, column=4, padx=(20, 10))

    rInfo = tk.Label(roomInfo
                     , text="Bed Type:"
                     , bg="white"
                     )
    rInfo.grid(row=0, column=5, padx=(20,10))
    rInfoEntry = tk.Entry(roomInfo
                          , bg="white"
                          , width=25
                          )
    rInfoEntry.grid(row=0, column=6)

    rStat = tk.Label(roomInfo
                     , text="Room Type:"
                     , bg="white"
                     )
    rStat.grid(row=1, column=5, padx=(20, 10), pady=(20, 0))
    rStatCombo = ttk.Combobox(roomInfo,
                         values=["Available", "Occupied", "Maintenance", "Under Construction", "Not Available"],
                         state="readonly",
                         font=("Arial", 10),
                         width=20)
    rStatCombo.grid(row=1, column=6, padx=(20, 10), pady=(20, 0))

    btnCreate = tk.Button(roomInfo
                          , text="Create"
                          , width=20
                          , pady=10
                          )
    btnCreate.grid(row=2, column=2, pady=(40,0))

    btnUpdate = tk.Button(roomInfo
                          , text="Update"
                          , width=20
                          , pady=10
                          )
    btnUpdate.grid(row=2, column=4, pady=(40, 0))

    btnDelete = tk.Button(roomInfo
                          , text="Delete"
                          , width=20
                          , pady=10
                          )
    btnDelete.grid(row=2, column=6, pady=(40, 0))




    treeRoomContainer = tk.Frame(mainBookingFrame
                             , width=1000
                             , height=400
                             , bg="white"
                             )
    treeRoomContainer.pack(padx=(13, 0), pady=5)
    treeRoomContainer.pack_propagate(False)

    # Treeview Widget
    treeRoom = ttk.Treeview(treeRoomContainer, show="headings", height=17)

    # Columns
    treeRoom['columns'] = ("RoomNumber"
                           , "RoomType"
                           , "BedType"
                           , "Status"
                       )

    # Formatting Columns
    treeRoom.column("RoomType"
                , anchor=tk.W
                , width=200
                )
    treeRoom.column("RoomNumber"
                    , anchor=tk.W
                    , width=200
                    )
    treeRoom.column("BedType"
                    , anchor=tk.W
                    , width=200
                    )
    treeRoom.column("Status"
                    , anchor=tk.W
                    , width=200
                    )

    # Create Headings
    treeRoom.heading("RoomNumber"
                 , text="Room Number"
                 , anchor=tk.W
                 )
    treeRoom.heading("RoomType"
                     , text="Room Type"
                     , anchor=tk.W
                     )
    treeRoom.heading("BedType"
                     , text="Bed Type"
                     , anchor=tk.W
                     )
    treeRoom.heading("Status"
                     , text="Status"
                     , anchor=tk.W
                     )

    # Pack
    treeRoom.pack(pady=(10, 0), padx=(10, 0), anchor="nw")

    return frame

def modelRoomCreate():
    # Note:
    # Scroll_Canvas - is the scrollable area, the actual Canvas widget that can scroll.
    # mainBookingFrame - The contents placed in the canvas, holding widgets. It doesn't scroll itself
    #                     it is moved around by canvas.

    # Main Whole Frame
    frame = tk.Frame(canvas
                     , bg="white"
                     , height=635
                     , width=1050
                     )
    # This forces the frame to keep the fixed size regardless what's inside of it.
    frame.pack_propagate(False)

    # A scrollable canvas embedded in the bookingFrame and a scrollbar
    scroll_canvas = tk.Canvas(frame, width=1050, bg="white")
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=scroll_canvas.yview)

    # Linking the canvas to the scrollbar so
    # when the canvas moves the scrollbar's thumb pos will also move.
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    # expand=True means the canvas will grow as the BookingFrame grows.
    scroll_canvas.pack(side="left", fill="both", expand=True)

    # This frame contains the actual scrollable contents
    mainBookingFrame = tk.Frame(scroll_canvas, bg="white")
    # Embedding the mainBookingFrame to the scroll canvas
    scroll_canvas.create_window((0, 0), window=mainBookingFrame, anchor="nw")

    # Events

    # This allows the canvas to know that the scrollable area has a specified tall
    # so that it can be updated or be scrolled
    def update_scrollregion(e):
        canvas_height = scroll_canvas.winfo_height()
        content_bbox = scroll_canvas.bbox("all")

        if content_bbox:
            content_height = content_bbox[3] - content_bbox[1]  # bottom - top

            # Only set scrollregion if content is taller than the canvas
            if content_height > canvas_height:
                scroll_canvas.configure(scrollregion=content_bbox)
            else:
                # Lock scrolling — set scrollregion to visible canvas only
                scroll_canvas.configure(scrollregion=(0, 0, 0, canvas_height))

    # Whenever the frame changes size,
    # it Recalculates the scroll region when the mainBookingFrame size changes
    mainBookingFrame.bind("<Configure>", update_scrollregion)

    def on_mousewheel(e):
        content_bbox = scroll_canvas.bbox("all")
        if content_bbox:
            content_height = content_bbox[3] - content_bbox[1]
            canvas_height = scroll_canvas.winfo_height()

            if content_height > canvas_height:
                scroll_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

    scroll_canvas.bind("<Enter>", lambda e: scroll_canvas.bind_all("<MouseWheel>", on_mousewheel))
    scroll_canvas.bind("<Leave>", lambda e: scroll_canvas.unbind_all("<MouseWheel>"))

    # Main UI Elements inside

    lblTitle = tk.Label(mainBookingFrame
                        , text="Create A Room"
                        , fg="black"
                        , bg="white"
                        , font=tkFont.Font(family="Arial"
                                           , size=21
                                           , weight="bold"
                                           )
                        )
    lblTitle.pack(pady=(20, 0)
                  , padx=(20, 0)
                  , anchor="w"
                  )

    # ======================= ROOM TYPE INFO ===============================

    roomTypeInfo = tk.LabelFrame(mainBookingFrame
                                 , text="Room Type Creation"
                                 , padx=20
                                 , pady=20
                                 , bg="white"
                                 , font=tkFont.Font(family="Arial"
                                                    , size=12
                                                    , weight="bold"
                                                    )
                                 )
    roomTypeInfo.pack(padx=20
                      , pady=20
                      , anchor="nw"
                      )

    rType = tk.Label(roomTypeInfo
                     , text="Room Type:"
                     , bg="white"
                     , anchor="w"
                     )
    rType.grid(row=0, column=1, padx=(0, 10))
    rTypeEntry = tk.Entry(roomTypeInfo
                          , bg="white"
                          , width=25
                          )
    rTypeEntry.grid(row=0, column=2)

    btnCreate = tk.Button(roomTypeInfo
                          , text="Create"
                          , width=20
                          , pady=10
                          )
    btnCreate.grid(row=1, column=2, pady=(20, 0))

    btnUpdate = tk.Button(roomTypeInfo
                          , text="Update"
                          , width=20
                          , pady=10
                          )
    btnUpdate.grid(row=1, column=4, pady=(20, 0), padx=(20, 0))

    btnDelete = tk.Button(roomTypeInfo
                          , text="Delete"
                          , width=20
                          , pady=10
                          )
    btnDelete.grid(row=1, column=6, pady=(20, 0), padx=(20, 0))

    treeContainer = tk.Frame(mainBookingFrame
                             , width=1000
                             , height=400
                             , bg="white"
                             )
    treeContainer.pack(padx=(13, 0), pady=5)
    treeContainer.pack_propagate(False)

    # Treeview Widget
    tree = ttk.Treeview(treeContainer, show="headings", height=17)

    # Columns
    tree['columns'] = ("RoomType"
                       )

    # Formatting Columns
    tree.column("RoomType"
                , anchor=tk.W
                , width=650
                )

    # Create Headings
    tree.heading("RoomType"
                 , text="Room Type"
                 , anchor=tk.W
                 )

    # Pack
    tree.pack(pady=(5, 0), padx=(10, 0), anchor="nw")

    # ======================= ROOM INFO ===============================

    roomInfo = tk.LabelFrame(mainBookingFrame
                             , text="Room Creation"
                             , padx=20
                             , pady=20
                             , bg="white"
                             , font=tkFont.Font(family="Arial"
                                                , size=12
                                                , weight="bold"
                                                )
                             )
    roomInfo.pack(padx=20
                  , pady=20
                  , anchor="nw"
                  )

    rNumber = tk.Label(roomInfo
                       , text="Room Number:"
                       , bg="white"
                       , anchor="w"
                       )
    rNumber.grid(row=0, column=1, padx=(0, 10))
    rNumberEntry = tk.Entry(roomInfo
                            , bg="white"
                            , width=25
                            )
    rNumberEntry.grid(row=0, column=2)

    rTypeSelect = tk.Label(roomInfo
                           , text="Room Type:"
                           , bg="white"
                           )
    rTypeSelect.grid(row=0, column=3, padx=(20, 10))
    rTypeCombo = ttk.Combobox(roomInfo,
                              values=["Single", "Double", "Family"],
                              state="readonly",
                              font=("Arial", 10),
                              width=25
                              )
    rTypeCombo.grid(row=0, column=4, padx=(20, 10))

    rInfo = tk.Label(roomInfo
                     , text="Bed Type:"
                     , bg="white"
                     )
    rInfo.grid(row=0, column=5, padx=(20, 10))
    rInfoEntry = tk.Entry(roomInfo
                          , bg="white"
                          , width=25
                          )
    rInfoEntry.grid(row=0, column=6)

    rStat = tk.Label(roomInfo
                     , text="Room Type:"
                     , bg="white"
                     )
    rStat.grid(row=1, column=5, padx=(20, 10), pady=(20, 0))
    rStatCombo = ttk.Combobox(roomInfo,
                              values=["Available", "Occupied", "Maintenance", "Under Construction",
                                      "Not Available"],
                              state="readonly",
                              font=("Arial", 10),
                              width=20)
    rStatCombo.grid(row=1, column=6, padx=(20, 10), pady=(20, 0))

    btnCreate = tk.Button(roomInfo
                          , text="Create"
                          , width=20
                          , pady=10
                          )
    btnCreate.grid(row=2, column=2, pady=(40, 0))

    btnUpdate = tk.Button(roomInfo
                          , text="Update"
                          , width=20
                          , pady=10
                          )
    btnUpdate.grid(row=2, column=4, pady=(40, 0))

    btnDelete = tk.Button(roomInfo
                          , text="Delete"
                          , width=20
                          , pady=10
                          )
    btnDelete.grid(row=2, column=6, pady=(40, 0))

    treeRoomContainer = tk.Frame(mainBookingFrame
                                 , width=1000
                                 , height=400
                                 , bg="white"
                                 )
    treeRoomContainer.pack(padx=(13, 0), pady=5)
    treeRoomContainer.pack_propagate(False)

    # Treeview Widget
    treeRoom = ttk.Treeview(treeRoomContainer, show="headings", height=17)

    # Columns
    treeRoom['columns'] = ("RoomNumber"
                           , "RoomType"
                           , "BedType"
                           , "Status"
                           )

    # Formatting Columns
    treeRoom.column("RoomType"
                    , anchor=tk.W
                    , width=200
                    )
    treeRoom.column("RoomNumber"
                    , anchor=tk.W
                    , width=200
                    )
    treeRoom.column("BedType"
                    , anchor=tk.W
                    , width=200
                    )
    treeRoom.column("Status"
                    , anchor=tk.W
                    , width=200
                    )

    # Create Headings
    treeRoom.heading("RoomNumber"
                     , text="Room Number"
                     , anchor=tk.W
                     )
    treeRoom.heading("RoomType"
                     , text="Room Type"
                     , anchor=tk.W
                     )
    treeRoom.heading("BedType"
                     , text="Bed Type"
                     , anchor=tk.W
                     )
    treeRoom.heading("Status"
                     , text="Status"
                     , anchor=tk.W
                     )

    # Pack
    treeRoom.pack(pady=(10, 0), padx=(10, 0), anchor="nw")

    return frame

def modelPricing():
    # Note:
    # Scroll_Canvas - is the scrollable area, the actual Canvas widget that can scroll.
    # mainBookingFrame - The contents placed in the canvas, holding widgets. It doesn't scroll itself
    #                     it is moved around by canvas.

    # Main Whole Frame
    frame = tk.Frame(canvas
                     , bg="white"
                     , height=635
                     , width=1050
                     )
    # This forces the frame to keep the fixed size regardless what's inside of it.
    frame.pack_propagate(False)

    # A scrollable canvas embedded in the bookingFrame and a scrollbar
    scroll_canvas = tk.Canvas(frame, width=1050, bg="white")
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=scroll_canvas.yview)

    # Linking the canvas to the scrollbar so
    # when the canvas moves the scrollbar's thumb pos will also move.
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    # expand=True means the canvas will grow as the BookingFrame grows.
    scroll_canvas.pack(side="left", fill="both", expand=True)

    # This frame contains the actual scrollable contents
    mainBookingFrame = tk.Frame(scroll_canvas, bg="white")
    # Embedding the mainBookingFrame to the scroll canvas
    scroll_canvas.create_window((0, 0), window=mainBookingFrame, anchor="nw")

    # Events

    # This allows the canvas to know that the scrollable area has a specified tall
    # so that it can be updated or be scrolled
    def update_scrollregion(e):
        canvas_height = scroll_canvas.winfo_height()
        content_bbox = scroll_canvas.bbox("all")

        if content_bbox:
            content_height = content_bbox[3] - content_bbox[1]  # bottom - top

            # Only set scrollregion if content is taller than the canvas
            if content_height > canvas_height:
                scroll_canvas.configure(scrollregion=content_bbox)
            else:
                # Lock scrolling — set scrollregion to visible canvas only
                scroll_canvas.configure(scrollregion=(0, 0, 0, canvas_height))

    # Whenever the frame changes size,
    # it Recalculates the scroll region when the mainBookingFrame size changes
    mainBookingFrame.bind("<Configure>", update_scrollregion)

    def on_mousewheel(e):
        content_bbox = scroll_canvas.bbox("all")
        if content_bbox:
            content_height = content_bbox[3] - content_bbox[1]
            canvas_height = scroll_canvas.winfo_height()

            if content_height > canvas_height:
                scroll_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

    scroll_canvas.bind("<Enter>", lambda e: scroll_canvas.bind_all("<MouseWheel>", on_mousewheel))
    scroll_canvas.bind("<Leave>", lambda e: scroll_canvas.unbind_all("<MouseWheel>"))

    # Main UI Elements inside

    lblTitle = tk.Label(mainBookingFrame
                        , text="Setup your Pricing"
                        , fg="black"
                        , bg="white"
                        , font=tkFont.Font(family="Arial"
                                           , size=21
                                           , weight="bold"
                                           )
                        )
    lblTitle.pack(pady=(20, 0)
                  , padx=(20, 0)
                  , anchor="w"
                  )

    # ======================= ROOM TYPE - BASE PRICING ===============================

    roomTypeInfo = tk.LabelFrame(mainBookingFrame
                                 , text="Pricing"
                                 , padx=20
                                 , pady=20
                                 , bg="white"
                                 , font=tkFont.Font(family="Arial"
                                                    , size=12
                                                    , weight="bold"
                                                    )
                                 )
    roomTypeInfo.pack(padx=20
                      , pady=20
                      , anchor="nw"
                      )

    rType = tk.Label(roomTypeInfo
                     , text="Room Type:"
                     , bg="white"
                     , anchor="w"
                     )
    rType.grid(row=0, column=1, padx=(0, 10))
    rTypeEntry = tk.Entry(roomTypeInfo
                          , bg="white"
                          , width=25
                          , state="readonly"
                          )
    rTypeEntry.grid(row=0, column=2)

    amount = tk.Label(roomTypeInfo
                     , text="Base Amount:"
                     , bg="white"
                     , anchor="w"
                     )
    amount.grid(row=0, column=3, padx=(0, 10))
    amountEntry = tk.Entry(roomTypeInfo
                          , bg="white"
                          , width=25
                          )
    amountEntry.grid(row=0, column=4)

    btnUpdate = tk.Button(roomTypeInfo
                          , text="Update"
                          , width=20
                          , pady=10
                          )
    btnUpdate.grid(row=1, column=2, pady=(20, 0), padx=(20, 0))


    treeContainer = tk.Frame(mainBookingFrame
                             , width=1000
                             , height=400
                             , bg="white"
                             )
    treeContainer.pack(padx=(13, 0), pady=5)
    treeContainer.pack_propagate(False)

    # Treeview Widget
    tree = ttk.Treeview(treeContainer, show="headings", height=17)

    # Columns
    tree['columns'] = ("RoomType"
                       , "BaseAmount"
                       )

    # Formatting Columns
    tree.column("RoomType"
                , anchor=tk.W
                , width=400
                )
    tree.column("BaseAmount"
                , anchor=tk.W
                , width=400
                )

    # Create Headings
    tree.heading("RoomType"
                 , text="Room Type"
                 , anchor=tk.W
                 )
    tree.heading("BaseAmount"
                 , text="Base Amount"
                 , anchor=tk.W
                 )

    # Pack
    tree.pack(pady=(5, 0), padx=(10, 0), anchor="nw")

    # ======================= ROOM INFO ===============================

    roomInfo = tk.LabelFrame(mainBookingFrame
                             , text="Discount Rules"
                             , padx=20
                             , pady=20
                             , bg="white"
                             , font=tkFont.Font(family="Arial"
                                                , size=12
                                                , weight="bold"
                                                )
                             )
    roomInfo.pack(padx=20
                  , pady=20
                  , anchor="nw"
                  )

    rNumber = tk.Label(roomInfo
                       , text="Discount Condition:"
                       , bg="white"
                       , anchor="w"
                       )
    rNumber.grid(row=0, column=1, padx=(0, 10))
    rNumberEntry = tk.Entry(roomInfo
                            , bg="white"
                            , width=25
                            )
    rNumberEntry.grid(row=0, column=2)

    rInfo = tk.Label(roomInfo
                     , text="Discount Percentage:"
                     , bg="white"
                     )
    rInfo.grid(row=0, column=3, padx=(20, 10))
    rInfoEntry = tk.Entry(roomInfo
                          , bg="white"
                          , width=25
                          )
    rInfoEntry.grid(row=0, column=4)

    btnCreateDisc = tk.Button(roomInfo
                          , text="Create"
                          , width=20
                          , pady=10
                          )
    btnCreateDisc.grid(row=1, column=2, pady=(20, 0), padx=(0, 0))

    btnUpdateDisc = tk.Button(roomInfo
                              , text="Update"
                              , width=20
                              , pady=10
                              )
    btnUpdateDisc.grid(row=1, column=3, pady=(20, 0), padx=(20, 0))

    btnDeleteDisc = tk.Button(roomInfo
                              , text="Delete"
                              , width=20
                              , pady=10
                              )
    btnDeleteDisc.grid(row=1, column=4, pady=(20, 0), padx=(20, 0))

    treeRoomContainer = tk.Frame(mainBookingFrame
                                 , width=1000
                                 , height=400
                                 , bg="white"
                                 )
    treeRoomContainer.pack(padx=(13, 0), pady=5)
    treeRoomContainer.pack_propagate(False)

    # Treeview Widget
    treeRoom = ttk.Treeview(treeRoomContainer, show="headings", height=17)

    # Columns
    treeRoom['columns'] = ("DiscountCondition"
                           , "DiscountPercent"
                           )

    # Formatting Columns
    treeRoom.column("DiscountCondition"
                    , anchor=tk.W
                    , width=400
                    )
    treeRoom.column("DiscountPercent"
                    , anchor=tk.W
                    , width=400
                    )

    # Create Headings
    treeRoom.heading("DiscountCondition"
                     , text="Discount Condition"
                     , anchor=tk.W
                     )
    treeRoom.heading("DiscountPercent"
                     , text="Discount Percent"
                     , anchor=tk.W
                     )

    # Pack
    treeRoom.pack(pady=(10, 0), padx=(10, 0), anchor="nw")


    return frame









# Main System

# Size of the Window Application
windowHeight = 720
windowWidth = 1280


# ============================ ENTRY POINT ==============================
root = tk.Tk()
root.title("Hotel Management - Admin")

# Updates the Window Size and gives accurate results to screen width and height
root.update_idletasks()
centerScreen()
root.resizable(False, False)



# Canvas Definition
canvas = tk.Canvas(root
                   , width = windowWidth
                   , height = windowHeight
                   , bg = "white"
                   )
canvas.pack( fill="both"
             , expand = True
             )



DASHBOARD_FRAME = modelDashboardFrame()
TOP_FRAME = modelTopFrame()
AD_ROOMSTAT_FRAME = modelRoomStatus()
AD_HISTORY_FRAME = modelHistoryFrame()
AD_IDCREATE_FRAME = modelIDCreate()
AD_ROOMCREATE_FRAME = modelRoomCreate()
AD_PRICING_FRAME = modelPricing()




id1 = canvas.create_window( windowWidth // 2
                      , 0
                      , window=TOP_FRAME
                      , anchor="n"
                      )

id2 = canvas.create_window( 0
                      , windowHeight // 2
                      , window=DASHBOARD_FRAME
                      , anchor="w"
                      )

id3 = canvas.create_window( 230
                      , windowHeight // 2 + 42
                      , window=AD_ROOMSTAT_FRAME
                      , anchor="w"
                      )

id4 = canvas.create_window( 230
                      , windowHeight // 2 + 42
                      , window=AD_HISTORY_FRAME
                      , anchor="w"
                      )

id5 = canvas.create_window( 230
                      , windowHeight // 2 + 42
                      , window=AD_IDCREATE_FRAME
                      , anchor="w"
                      )

id6 = canvas.create_window( 230
                      , windowHeight // 2 + 42
                      , window=AD_ROOMCREATE_FRAME
                      , anchor="w"
                      )

id7 = canvas.create_window( 230
                      , windowHeight // 2 + 42
                      , window=AD_PRICING_FRAME
                      , anchor="w"
                      )


# Canvas Config
AD_ROOMSTAT_FRAME.lift()




















# Application Loop
root.mainloop()

