import tkinter as tk
from email.policy import default
from tkinter import messagebox as mb, StringVar, messagebox
from tkinter import ttk
import tkinter.font as tkFont
from tkcalendar import DateEntry

import sqlite3
import os

# Classes
from Classes.admin.IDService import IDService
from Classes.admin.RoomTypeService import RoomTypeService

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



# MODELS

def createRoomSQL(roomNumber, roomType, bedType, roomCapacity, status, basePrice):
    try:
        # Get the absolute path of this script file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Build the path to the database file
        db_path = os.path.join(script_dir, '..', 'Database', 'hotelManagement.db')
        # Normalize the path (handle ../ correctly)
        db_path = os.path.normpath(db_path)

        conn = sqlite3.connect(db_path)

        cursor = conn.cursor()

        createRoom = """
                INSERT INTO ROOM (RoomNumber, RoomType, BedType, RoomCapacity, Status, Base_Price)
                VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(createRoom, (roomNumber, roomType, bedType, roomCapacity, status, basePrice))
        conn.commit()

        cursor.close()
        conn.close()
    except Exception as e:
        print("Error conttecting to database:", e)
        return None

def loadRoomSQL(tree):
    try:
        # Get the absolute path of this script file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Build the path to the database file
        db_path = os.path.join(script_dir, '..', 'Database', 'hotelManagement.db')
        # Normalize the path (handle ../ correctly)
        db_path = os.path.normpath(db_path)

        conn = sqlite3.connect(db_path)

        cursor = conn.cursor()

        loadRooms = """
                SELECT RoomID, RoomNumber, RoomType, BedType, RoomCapacity, Status
                FROM ROOM
        """

        # Execute and Fetch
        cursor.execute(loadRooms)
        rows = cursor.fetchall()

        # Insert into Treeview
        for row in rows:
            roomID = row[0]  # Assuming RoomID is the first column
            tree.insert("", "end", iid=str(roomID), values=row)

        # Close
        cursor.close()
        conn.close()

    except Exception as e:
        print("Error connecting to database:", e)
        return None

def deleteRoomSQL(tree):
    try:
        selected_item = tree.selection()

        # Get the absolute path of this script file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Build the path to the database file
        db_path = os.path.join(script_dir, '..', 'Database', 'hotelManagement.db')
        # Normalize the path (handle ../ correctly)
        db_path = os.path.normpath(db_path)

        conn = sqlite3.connect(db_path)

        cursor = conn.cursor()

        row_values = tree.item(selected_item)["values"]
        print("Selected row values:", row_values)

        roomID = int(row_values[0])


        # Delete from SQLite
        cursor.execute("DELETE FROM ROOM WHERE RoomID = ?", (roomID,))
        conn.commit()

        # Delete from Treeview
        tree.delete(selected_item)

        # Close
        cursor.close()
        conn.close()

    except Exception as e:
        print("Error connecting to database:", e)
        return None



def modelTopFrame():

    topFrame = tk.Frame(canvas
                        , bg=TOP_FRAME_COLOR
                        , height=85
                        , width=windowWidth
                        )
    topFrame.pack_propagate(False)

    lblTitle = tk.Label(topFrame
                        , text="Hotel Management"
                        , fg="White"
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
        btnRoomStatus.config(bg="#2ecc71"
                         , fg="white"
                         )
        btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="#BBBBBB"
                             )
        btnIDCreate.config(bg=DASHBOARD_FRAME_COLOR
                           , fg="#BBBBBB"
                           )
        btnRoomCreate.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="#BBBBBB"
                             )

    def onHistoryClick():
        AD_HISTORY_FRAME.lift()
        btnHistory.config(bg="#2ecc71"
                         , fg="white"
                         )
        btnRoomStatus.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="#BBBBBB"
                             )
        btnIDCreate.config(bg=DASHBOARD_FRAME_COLOR
                           , fg="#BBBBBB"
                           )
        btnRoomCreate.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="#BBBBBB"
                             )
        btnPricing.config(bg=DASHBOARD_FRAME_COLOR
                          , fg="#BBBBBB"
                          )

    def onIDCreateClick():
        AD_IDCREATE_FRAME.lift()
        btnIDCreate.config(bg="#2ecc71"
                         , fg="white"
                         )
        btnRoomStatus.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="#BBBBBB"
                             )
        btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                          , fg="#BBBBBB"
                          )
        btnRoomCreate.config(bg=DASHBOARD_FRAME_COLOR
                           , fg="#BBBBBB"
                           )
        btnPricing.config(bg=DASHBOARD_FRAME_COLOR
                          , fg="#BBBBBB"
                          )

    def onRoomCreateClick():
        AD_ROOMCREATE_FRAME.lift()
        btnRoomCreate.config(bg="#2ecc71"
                         , fg="white"
                         )
        btnRoomStatus.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="#BBBBBB"
                             )
        btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                          , fg="#BBBBBB"
                          )
        btnIDCreate.config(bg=DASHBOARD_FRAME_COLOR
                           , fg="#BBBBBB"
                           )
        btnPricing.config(bg=DASHBOARD_FRAME_COLOR
                           , fg="#BBBBBB"
                           )

    def onPricingClick():
        AD_PRICING_FRAME.lift()
        btnPricing.config(bg="#2ecc71"
                         , fg="white"
                         )
        btnRoomStatus.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="#BBBBBB"
                             )
        btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                          , fg="#BBBBBB"
                          )
        btnIDCreate.config(bg=DASHBOARD_FRAME_COLOR
                           , fg="#BBBBBB"
                           )
        btnRoomCreate.config(bg=DASHBOARD_FRAME_COLOR
                           , fg="#BBBBBB"
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
                            , bg="red"
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

    treeContainer = tk.Frame(mainFrame,
                             width=1000,
                             height=400,
                             bg="white")
    treeContainer.pack(padx=10, pady=10, fill="x", expand=True)
    treeContainer.pack_propagate(False)

    # Treeview Widget
    roomTree = ttk.Treeview(treeContainer, show="headings", height=17)

    # Columns
    roomTree['columns'] = ("Room Number", "Room Type", "Bed Type", "Status")

    # Stretch Treeview to fill container
    roomTree.pack(fill="both", expand=True)  # ✅ this makes it match treeContainer's width

    # Optional: Make columns auto-stretch to fill width
    roomTree.column("Room Number", anchor="center", width=150, stretch=True)
    roomTree.column("Room Type", anchor="center", width=200, stretch=True)
    roomTree.column("Bed Type", anchor="center", width=200, stretch=True)
    roomTree.column("Status", anchor="center", width=100, stretch=True)

    # (Optional) Set column headings
    roomTree.heading("Room Number", text="Room Number")
    roomTree.heading("Room Type", text="Room Type")
    roomTree.heading("Bed Type", text="Bed Type")
    roomTree.heading("Status", text="Status")

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

    # The Json CRUD Functionality
    logic = IDService()

    # Methods

    selected_index = [None]  # Mutable container for selected index

    def refresh():
        for i in tree.get_children():
            tree.delete(i)
        for idx, name in enumerate(logic.read_all()):
            tree.insert('', 'end', iid=str(idx), values=(name,))

    def clear():
        dataEntry.delete(0, tk.END)
        selected_index[0] = None  # Reset selection on clear

    def on_select(e):
        selected = tree.focus()
        if selected:
            selected_index[0] = int(selected)
            name = tree.item(selected, 'values')[0]
            dataEntry.delete(0, tk.END)
            dataEntry.insert(0, name)
        else:
            selected_index[0] = None

    def add():
        name = dataEntry.get().strip()
        if not name:
            messagebox.showwarning("Missing", "Name is required.")
            return
        if selected_index[0] is not None:
            data = logic.read_all()
            if selected_index[0] < len(data) and data[selected_index[0]] == name:
                messagebox.showwarning("Duplicate", "This item is already selected. Use Update instead.")
                return
        success, msg = logic.add(name)
        if success:
            refresh()
            clear()
        else:
            messagebox.showerror("Error", msg)

    def update():
        if selected_index[0] is None:
            messagebox.showinfo("Select", "Select an entry to update.")
            return
        name = dataEntry.get().strip()
        if not name:
            messagebox.showwarning("Missing", "Name is required.")
            return
        data = logic.read_all()
        if selected_index[0] < len(data) and data[selected_index[0]] == name:
            messagebox.showinfo("No changes", "The name is the same as before.")
            return
        success, msg = logic.update(selected_index[0], name)
        if success:
            refresh()
            clear()
        else:
            messagebox.showerror("Error", msg)

    def delete():
        selected = tree.focus()
        if not selected:
            messagebox.showinfo("Select", "Select an entry to delete.")
            return
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this?")
        if confirm:
            success, msg = logic.delete(int(selected))
            if success:
                refresh()
                clear()
            else:
                messagebox.showerror("Error", msg)






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
                          , command = add
                          )
    btnAdd.pack(pady=(20, 0), padx=(15, 0), side="left", anchor="w")

    btnUpdate = tk.Button(btnFrame
                          , text="Update"
                          , pady=5
                          , padx=40
                          , command = update
                          )
    btnUpdate.pack(pady=(20, 0), padx=(20, 0), side="left", anchor="w")

    btnDelete = tk.Button(btnFrame
                          , text="Delete"
                          , pady=5
                          , padx=40
                          , command = delete
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

    # Event Binding
    tree.bind("<<TreeviewSelect>>", on_select)
    refresh()

    return frame

def modelRoomCreate():

    # The Json CRUD Functionality
    logic = RoomTypeService()

    # Methods

    selected_index = [None]  # Mutable container for selected index

    def rts_refresh():
        for i in tree.get_children():
            tree.delete(i)
        for idx, item in enumerate(logic.read_all()):
            # Insert the 'name' in the treeview columns
            tree.insert('', 'end', iid=str(idx), values=(item['name']))

    def rts_clear():
        rTypeEntry.delete(0, tk.END)
        selected_index[0] = None  # Reset selection on clear

    def rts_on_select(e):
        selected = tree.focus()
        if selected:
            selected_index[0] = int(selected)
            name = tree.item(selected, 'values')[0]
            rTypeEntry.delete(0, tk.END)
            rTypeEntry.insert(0, name)
        else:
            selected_index[0] = None

    def rts_add():
        name = rTypeEntry.get().strip()
        if not name:
            messagebox.showwarning("Missing", "Name is required.")
            return
        if selected_index[0] is not None:
            data = logic.read_all()
            if selected_index[0] < len(data) and data[selected_index[0]]['name'] == name:
                messagebox.showwarning("Duplicate", "This item is already selected. Use Update instead.")
                return
        success, msg = logic.add(name, 0)
        if success:
            rts_refresh()
            rts_clear()
            roomTypeCmbRefresh()
        else:
            messagebox.showerror("Error", msg)

    def rts_update():
        if selected_index[0] is None:
            messagebox.showinfo("Select", "Select an entry to update.")
            return
        name = rTypeEntry.get().strip()
        if not name:
            messagebox.showwarning("Missing", "Name is required.")
            return
        data = logic.read_all()
        if selected_index[0] < len(data) and data[selected_index[0]]['name'] == name:
            messagebox.showinfo("No changes", "The name is the same as before.")
            return
        success, msg = logic.update(selected_index[0], name, 0)
        if success:
            rts_refresh()
            rts_clear()
            roomTypeCmbRefresh()
        else:
            messagebox.showerror("Error", msg)

    def rts_delete():
        selected = tree.focus()
        if not selected:
            messagebox.showinfo("Select", "Select an entry to delete.")
            return
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this?")
        if confirm:
            success, msg = logic.delete(int(selected))
            if success:
                rts_refresh()
                rts_clear()
            else:
                messagebox.showerror("Error", msg)

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
                      , anchor="nw"
                      , fill="x"
                      , expand=True
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

    btnCreateRT = tk.Button(roomTypeInfo
                            , text="Create"
                            , width=20
                            , pady=10
                            , bg="#3498db"
                            , fg="white"
                            , activebackground="#2980b9"
                            , font=tkFont.Font(size=10, weight="bold")
                            , command=lambda: rts_add()
                            )
    btnCreateRT.grid(row=1, column=2, pady=(20, 0))

    btnUpdateRT = tk.Button(roomTypeInfo
                            , text="Update"
                            , width=20
                            , pady=10
                            , bg="#27ae60"
                            , fg="white"
                            , activebackground="#1e8449"
                            , font=tkFont.Font(size=10, weight="bold")
                            , command=rts_update
                            )
    btnUpdateRT.grid(row=1, column=4, pady=(20, 0), padx=(20, 0))

    btnDeleteRT = tk.Button(roomTypeInfo
                            , text="Delete"
                            , width=20
                            , pady=10
                            , bg="#e74c3c"
                            , fg="white"
                            , activebackground="#c0392b"
                            , font=tkFont.Font(size=10, weight="bold")
                            , command=rts_delete
                            )
    btnDeleteRT.grid(row=1, column=6, pady=(20, 0), padx=(20, 0))

    treeContainer = tk.Frame(mainBookingFrame
                             , width=1000
                             , height=400
                             , bg="white"
                             )
    treeContainer.pack(padx=(13, 20), pady=5, fill="x", expand=True)
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
                , stretch=True
                )

    # Create Headings
    tree.heading("RoomType"
                 , text="Room Type"
                 , anchor=tk.W
                 )

    # Pack
    tree.pack(pady=(5, 0)
              , padx=(10, 0)
              , fill="both"
              , expand=True
              , anchor="nw"
              )

    # Tree Config
    tree.bind("<<TreeviewSelect>>", rts_on_select)
    rts_refresh()

    # ======================= ROOM INFO ===============================

    roomInfo = tk.LabelFrame(mainBookingFrame
                             , text="Room Creation"
                             , padx=20
                             , pady=20
                             , bg="white"
                             , font=tkFont.Font(family="Arial", size=12, weight="bold")
                             )
    roomInfo.pack(padx=20
                  , pady=20
                  , anchor="nw"
                  , fill="x"
                  , expand=True
                  )

    rNumber = tk.Label(roomInfo
                       , text="Room Number:"
                       , bg="white"
                       , anchor="w"
                       , font=tkFont.Font(size=10)
                       )
    rNumber.grid(row=0, column=1, padx=(0, 10))
    rNumberEntry = tk.Entry(roomInfo
                            , bg="white"
                            , width=25
                            , font=tkFont.Font(size=10)
                            )
    rNumberEntry.grid(row=0, column=2)

    rTypeSelect = tk.Label(roomInfo
                           , text="Room Type:"
                           , bg="white"
                           , font=tkFont.Font(size=10)
                           )
    rTypeSelect.grid(row=0, column=3, padx=(20, 10))
    rTypeCombo = ttk.Combobox(roomInfo,
                              state="readonly",
                              font=("Arial", 10),
                              width=25)
    rTypeCombo.grid(row=0, column=4, padx=(20, 10))

    def roomTypeCmbRefresh():
        roomTypeData = logic.read_all()
        roomTypes = [item['name'] for item in roomTypeData]
        rTypeCombo['values'] = roomTypes

    roomTypeCmbRefresh()

    btLabel = tk.Label(roomInfo
                       , text="Bed Type:"
                       , bg="white"
                       , font=tkFont.Font(size=10)
                       )
    btLabel.grid(row=0, column=5, padx=(20, 10))
    btEntry = tk.Entry(roomInfo
                       , bg="white"
                       , width=25
                       , font=tkFont.Font(size=10)
                       )
    btEntry.grid(row=0, column=6)

    rStat = tk.Label(roomInfo
                     , text="Status:"
                     , bg="white"
                     , font=tkFont.Font(size=10)
                     )
    rStat.grid(row=1, column=5, padx=(20, 10), pady=(20, 0))
    rStatCombo = ttk.Combobox(roomInfo,
                              values=["Available", "Occupied", "Maintenance", "Under Construction", "Not Available"],
                              state="readonly",
                              font=("Arial", 10),
                              width=20)
    rStatCombo.grid(row=1, column=6, padx=(20, 10), pady=(20, 0))

    rCapacity = tk.Label(roomInfo
                         , text="Room Capacity:"
                         , bg="white"
                         , font=tkFont.Font(size=10)
                         )
    rCapacity.grid(row=1, column=3, padx=(20, 10), pady=(27, 0))
    rCapacityEntry = tk.Entry(roomInfo
                              , bg="white"
                              , width=27
                              , font=tkFont.Font(size=10)
                              )
    rCapacityEntry.grid(row=1, column=4, pady=(25, 0))

    # METHODS ========================================
    def validateFields():
        selectRoomNumber = rNumberEntry.get().strip()
        selectBedType = btEntry.get().strip()
        selectRCapacity = rCapacityEntry.get().strip()

        if not selectBedType and not selectRoomNumber:
            messagebox.showwarning("Missing Data", "Please fill in all fields.")
            return

        # Check if capacity is numeric
        try:
            capacityValue = int(selectRCapacity)
        except ValueError:
            messagebox.showwarning("Invalid Data", "Capacity must be a whole number.")
            return

        # Create the Room
        createRoomRecord(capacityValue)


    def get_base_price_by_name(data, name):
        for item in data:
            if item['name'] == name:
                return item['base_price']
        return None  # or some default value if not found


    def createRoomRecord(capacityValue):
        selectRoomNumber = rNumberEntry.get().strip()
        selectBedType = btEntry.get().strip()
        selectRoomType = rTypeCombo.get()
        selectRStat = rStatCombo.get()
        selectRoomTypePrice = get_base_price_by_name(logic.read_all(), selectRoomType)

        createRoomSQL(selectRoomNumber, selectRoomType, selectBedType, capacityValue, selectRStat, selectRoomTypePrice)
        clearCreateRoomFields()
        messagebox.showinfo("Success", "Room added successfully!")
        loadRoomData()


    def clearCreateRoomFields():
        rNumberEntry.delete(0, tk.END)
        rTypeCombo.current(0)
        btEntry.delete(0, tk.END)
        rStatCombo.current(0)
        rCapacityEntry.delete(0, tk.END)
    # METHODS ========================================

    btnCreate = tk.Button(roomInfo
                          , text="Create"
                          , width=20
                          , pady=10
                          , command = validateFields
                          )
    btnCreate.grid(row=2, column=2, pady=(40,0))

    # METHODS ========================================

    def onRoomsSelect(e):
        selected = treeRoom.focus()  # get selected item's ID
        if selected:
            values = treeRoom.item(selected, 'values')
            rNumberEntry.delete(0, tk.END)
            rNumberEntry.insert(0, values[1])

            rTypeCombo.set(values[2])

            btEntry.delete(0, tk.END)
            btEntry.insert(0, values[3])

            rCapacityEntry.delete(0, tk.END)
            rCapacityEntry.insert(0, values[4])

            rStatCombo.set(values[5])

            btnCreate.config(state="disabled")


    def updateRoomRecord():
        selected = treeRoom.focus()
        if not selected:
            messagebox.showwarning("Select Room", "Please select a room to update.")
            return

        selectedID = treeRoom.selection()

        selectRoomType = rTypeCombo.get()
        selectRStat = rStatCombo.get()
        selectRoomNumber = rNumberEntry.get().strip()
        selectBedType = btEntry.get().strip()
        selectRCapacity = rCapacityEntry.get().strip()
        selectRoomID = int(selectedID[0])

        if not selectBedType and not selectRoomNumber:
            messagebox.showwarning("Missing Data", "Please fill in all fields.")
            return

        # Check if capacity is numeric
        try:
            capacityValue = int(selectRCapacity)
        except ValueError:
            messagebox.showwarning("Invalid Data", "Capacity must be a whole number.")
            return

        try:
            # Build the correct DB path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.normpath(os.path.join(script_dir, '..', 'Database', 'hotelManagement.db'))

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Update room using Room Number as primary identifier (assumed)
            cursor.execute("""
                    UPDATE ROOM
                    SET RoomNumber = ?, RoomType = ?, BedType = ?, RoomCapacity = ?,  Status = ?
                    WHERE RoomID = ?
                """, (selectRoomNumber, selectRoomType, selectBedType, capacityValue, selectRStat, selectRoomID))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Room updated successfully.")
            loadRoomData()  # Refresh tree
            clearCreateRoomFields() # Clear Room Fields
            btnCreate.config(state="normal") # Re-enable

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update room.\n{e}")


    def on_deselect():
        # Clear Treeview selection
        treeRoom.selection_remove(treeRoom.selection())
        # Clear Room Fields
        clearCreateRoomFields()
        # Enable Create button
        btnCreate.config(state="normal")


    def onDelete():
        selected = treeRoom.focus()
        if not selected:
            messagebox.showwarning("Select Room", "Please select a room to update.")
            return

        deleteRoomSQL(treeRoom)
        messagebox.showinfo("Deleted", f"Room deleted.")
        clearCreateRoomFields()
        btnCreate.config(state="normal")

    # METHODS ========================================

    btnUpdate = tk.Button(roomInfo
                          , text="Update"
                          , width=20
                          , pady=10
                          , command = updateRoomRecord
                          )
    btnUpdate.grid(row=2, column=4, pady=(40, 0))

    btnDelete = tk.Button(roomInfo
                          , text="Delete"
                          , width=20
                          , pady=10
                          , command = onDelete
                          )
    btnDelete.grid(row=2, column=6, pady=(40, 0))

    btnDeselect = tk.Button(roomInfo
                          , text="Deselect"
                          , width=20
                          , pady=10
                          , command = on_deselect
                          )
    btnDeselect.grid(row=3, column=6, pady=(20, 0))

    treeRoomContainer = tk.Frame(mainBookingFrame
                                 , width=1000
                                 , height=400
                                 , bg="white"
                                 )
    treeRoomContainer.pack(padx=(13, 20), pady=5, fill="x", expand=True)
    treeRoomContainer.pack_propagate(False)

    # Treeview Widget
    treeRoom = ttk.Treeview(treeRoomContainer, show="headings", height=17)

    # Columns
    treeRoom['columns'] = ("RoomID"
                           , "RoomNumber"
                           , "RoomType"
                           , "BedType"
                           , "RoomCapacity"
                           , "Status"
                           )

    # Formatting Columns
    treeRoom.column("RoomID"
                    , anchor=tk.W
                    , width=150
                    , stretch=True
                    )
    treeRoom.column("RoomNumber"
                    , anchor=tk.W
                    , width=150
                    , stretch=True
                    )
    treeRoom.column("RoomType"
                    , anchor=tk.W
                    , width=150
                    , stretch=True
                    )
    treeRoom.column("BedType"
                    , anchor=tk.W
                    , width=150
                    , stretch=True
                    )
    treeRoom.column("RoomCapacity"
                    , anchor=tk.W
                    , width=150
                    , stretch=True
                    )
    treeRoom.column("Status"
                    , anchor=tk.W
                    , width=150
                    , stretch=True
                    )

    # Create Headings
    treeRoom.heading("RoomID"
                     , text="Room ID"
                     , anchor=tk.W
                     )
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
    treeRoom.heading("RoomCapacity"
                     , text="Room Capacity"
                     , anchor=tk.W
                     )
    treeRoom.heading("Status"
                     , text="Status"
                     , anchor=tk.W
                     )

    # Pack Treeview fully inside the container
    treeRoom.pack(pady=(10, 0)
                  , padx=(10, 0)
                  , fill="both"
                  , expand=True
                  , anchor="nw"
                  )

    treeRoom.bind("<<TreeviewSelect>>", onRoomsSelect)

    # TREE VIEW METHODS ===========================================

    def loadRoomData():
        # Clear Existing Rows to avoid duplicates
        for item in treeRoom.get_children():
            treeRoom.delete(item)

        # Load new data
        loadRoomSQL(treeRoom)

    # TREE VIEW METHODS ===========================================

    # Load the Room Data from Database
    loadRoomData()

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
                      , fill="x"
                      , expand=True
                      )

    rType = tk.Label(roomTypeInfo
                     , text="Room Type:"
                     , bg="white"
                     , anchor="w"
                     , font=tkFont.Font(size=10)
                     )
    rType.grid(row=0, column=1, padx=(0, 10))
    rTypeEntry = tk.Entry(roomTypeInfo
                          , bg="white"
                          , width=25
                          , state="readonly"
                          , font=tkFont.Font(size=10)
                          )
    rTypeEntry.grid(row=0, column=2)

    amount = tk.Label(roomTypeInfo
                      , text="Base Amount:"
                      , bg="white"
                      , anchor="w"
                      , font=tkFont.Font(size=10)
                      )
    amount.grid(row=0, column=3, padx=(0, 10))
    amountEntry = tk.Entry(roomTypeInfo
                           , bg="white"
                           , width=25
                           , font=tkFont.Font(size=10)
                           )
    amountEntry.grid(row=0, column=4)

    btnUpdate = tk.Button(roomTypeInfo,
                          text="Update",
                          width=20,
                          pady=10,
                          bg="#059669",  # ✅ Emerald Green
                          fg="white",  # White text
                          activebackground="#047857",  # Darker green on hover
                          activeforeground="white",
                          font=tkFont.Font(size=10, weight="bold"),
                          relief=tk.FLAT,
                          cursor="hand2")

    # 🟢 Align to the right using grid
    btnUpdate.grid(row=1,
                   column=7,
                   sticky="n",
                   padx=(0, 20),
                   pady=(0, 0))

    treeContainer = tk.Frame(mainBookingFrame
                             , width=1000
                             , height=400
                             , bg="white"
                             )
    treeContainer.pack(padx=(13, 20), pady=5, fill="x", expand=True)
    treeContainer.pack_propagate(False)

    # Treeview Widget
    tree = ttk.Treeview(treeContainer, show="headings", height=17)

    # Columns
    tree['columns'] = ("RoomType", "BaseAmount")

    tree.column("RoomType"
                , anchor=tk.W
                , width=400
                , stretch=True
                )
    tree.column("BaseAmount"
                , anchor=tk.W
                , width=400
                , stretch=True
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

    # Pack Treeview
    tree.pack(pady=(5, 0)
              , padx=(10, 0)
              , fill="both"
              , expand=True
              , anchor="nw")

    # ======================= ROOM INFO ===============================

    roomInfo = tk.LabelFrame(mainBookingFrame,
                             text="Discount Rules",
                             padx=20,
                             pady=20,
                             bg="white",
                             bd=1,
                             relief="solid",
                             font=tkFont.Font(family="Arial", size=12, weight="bold"))
    roomInfo.pack(fill="x", padx=20, pady=20)  # ✅ Stretch full width

    # ✅ Make columns stretch if needed
    roomInfo.grid_columnconfigure(2, weight=1)
    roomInfo.grid_columnconfigure(4, weight=1)

    # Row 0 - Labels and Entry Fields
    rNumber = tk.Label(roomInfo,
                       text="Discount Condition:",
                       bg="white",
                       anchor="w")
    rNumber.grid(row=0, column=1, padx=(0, 10), sticky="e")

    rNumberEntry = tk.Entry(roomInfo,
                            bg="white",
                            width=30)
    rNumberEntry.grid(row=0, column=2, sticky="w")

    rInfo = tk.Label(roomInfo,
                     text="Discount Percentage:",
                     bg="white")
    rInfo.grid(row=0, column=3, padx=(20, 10), sticky="e")

    rInfoEntry = tk.Entry(roomInfo,
                          bg="white",
                          width=30)
    rInfoEntry.grid(row=0, column=4, sticky="w")

    # Row 1 - Buttons
    button_style = {
        "width": 20,
        "pady": 10,
        "bg": "#059669",
        "fg": "white",
        "activebackground": "#047857",
        "activeforeground": "white",
        "font": tkFont.Font(size=10, weight="bold"),
        "relief": tk.FLAT,
        "cursor": "hand2"
    }

    btnCreateDisc = tk.Button(roomInfo, text="Create", **button_style)
    btnCreateDisc.grid(row=1, column=2, pady=(20, 0), padx=(0, 0), sticky="e")

    btnUpdateDisc = tk.Button(roomInfo, text="Update", **button_style)
    btnUpdateDisc.grid(row=1, column=3, pady=(20, 0), padx=(20, 0))

    btnDeleteDisc = tk.Button(roomInfo, text="Delete", **button_style)
    btnDeleteDisc.grid(row=1, column=4, pady=(20, 0), padx=(20, 0), sticky="w")

    # ========== Treeview Section ==========

    treeRoomContainer = tk.Frame(mainBookingFrame,
                                 bg="white")
    treeRoomContainer.pack(fill="x", padx=20, pady=5)

    treeRoom = ttk.Treeview(treeRoomContainer, show="headings", height=17)

    treeRoom['columns'] = ("DiscountCondition", "DiscountPercent")

    treeRoom.column("DiscountCondition", anchor=tk.W, width=400)
    treeRoom.column("DiscountPercent", anchor=tk.W, width=400)

    treeRoom.heading("DiscountCondition", text="Discount Condition", anchor=tk.W)
    treeRoom.heading("DiscountPercent", text="Discount Percent", anchor=tk.W)

    treeRoom.pack(fill="x", padx=10, pady=(10, 0), anchor="nw")

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

