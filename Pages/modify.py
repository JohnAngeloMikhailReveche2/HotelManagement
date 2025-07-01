import tkinter as tk
from datetime import datetime
from tkinter import messagebox, StringVar
from tkinter import ttk
import tkinter.font as tkFont
from datetime import datetime, timedelta

import json
import os
import sys

import sqlite3

from Classes.admin.IDService import IDService
from Classes.admin.RoomTypeService import RoomTypeService


# Color HEX Constants
# https://www.color-hex.com/color-palette/1061596
TOP_FRAME_COLOR = "#1a3f73"
DASHBOARD_FRAME_COLOR = "#598dba"
DASHBOARD_BUTTON_COLOR = "#4d6b88"

# CONSTANTS
COLUMN_WIDTH = 100

# Mapping
roomIDMap = {}
guestID = 0
roomNumber = ""
pricePerHour = 0.0
durationPrice = 0.0
roomBasePrice = 0.0
checkInGlobal = datetime.now()
checkOutGlobal = datetime.now()





def openDetailWindow(rowData):
    root = tk.Toplevel

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

        btnBack = tk.Button(topFrame
                            , text="Back"
                            , padx=30
                            , pady=10
                            )
        btnBack.pack(pady=(20, 0)
                     , padx=(15, 0)
                     , anchor="w"
                     , side="left"
                     )

        lblTitle = tk.Label(topFrame
                            , text="Manage"
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
                      , side="left"
                      )

        return topFrame

    def modelMainFrame():

        logic = RoomTypeService()
        idLogic = IDService()

        # Combobox Event for Pricing and Check In and Out DateTime
        def update_booking_info(e=None):
            global checkInGlobal
            global checkOutGlobal

            try:
                hours = int(hour_cb.get())
                minutes = int(minute_cb.get())

                # Time Calculation
                checkinTime = datetime.now()
                checkoutTime = checkinTime + timedelta(hours=hours, minutes=minutes)
                totalTimeHours = hours + (minutes / 60)

                # Price Calculation
                total = totalTimeHours * pricePerHour

                # Set Values
                checkInLabel.config(text=checkinTime.strftime("%Y-%m-%d %I:%M %p"))
                checkOutLabel.config(text=checkoutTime.strftime("%Y-%m-%d %I:%M %p"))
                checkInGlobal = checkinTime
                checkOutGlobal = checkoutTime

                totalPriceEntry.config(state="normal")
                totalPriceEntry.delete(0, tk.END)
                totalPriceEntry.insert(0, f"{total}")
                totalPriceEntry.config(state="readonly")

                timePriceEntry.config(state="normal")
                timePriceEntry.delete(0, tk.END)
                timePriceEntry.insert(0, f"{total}")
                timePriceEntry.config(state="readonly")

                roomPriceEntry.config(state="normal")
                roomPriceEntry.delete(0, tk.END)
                roomPriceEntry.insert(0, f"{pricePerHour}")
                roomPriceEntry.config(state="readonly")

            except ValueError:
                pass


        frame = tk.Frame(canvas
                         , bg="white"
                         , height=windowHeight
                         , width=windowWidth
                         )
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
        # Embedding the mainFrame to the scroll canvas
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
        # it Recalculates the scroll region when the mainFrame size changes
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

        personalInfoGroupBox = tk.LabelFrame(mainFrame
                                             , text="Personal Information"
                                             , padx=20
                                             , pady=20
                                             , bg="white"
                                             , font=tkFont.Font(family="Arial"
                                                                , size=12
                                                                , weight="bold"
                                                                )
                                             )
        personalInfoGroupBox.pack(padx=20
                                  , pady=20
                                  )

        fName = tk.Label(personalInfoGroupBox
                         , text="First Name:"
                         , bg="white"
                         , anchor="w"
                         )
        fName.grid(row=0, column=1, padx=(0, 10))
        fNameEntry = tk.Entry(personalInfoGroupBox
                              , bg="white"
                              , width=25
                              )
        fNameEntry.grid(row=0, column=2)

        mName = tk.Label(personalInfoGroupBox
                         , text="Middle Name:"
                         , bg="white"
                         )
        mName.grid(row=0, column=3, padx=(20, 10))
        mNameEntry = tk.Entry(personalInfoGroupBox
                              , bg="white"
                              , width=25
                              )
        mNameEntry.grid(row=0, column=4)

        lName = tk.Label(personalInfoGroupBox
                         , text="Last Name:"
                         , bg="white"
                         )
        lName.grid(row=0, column=5, padx=(20, 10))
        lNameEntry = tk.Entry(personalInfoGroupBox
                              , bg="white"
                              , width=25
                              )
        lNameEntry.grid(row=0, column=6)

        phoneNum = tk.Label(personalInfoGroupBox
                            , text="Phone Number:"
                            , bg="white"
                            )
        phoneNum.grid(row=1, column=1, padx=(0, 10), pady=(20, 0))
        phoneNumEntry = tk.Entry(personalInfoGroupBox
                                 , bg="white"
                                 , width=25
                                 )
        phoneNumEntry.grid(row=1, column=2, pady=(20, 0))

        gender = tk.Label(personalInfoGroupBox
                          , text="Gender:"
                          , bg="white"
                          )
        gender.grid(row=1, column=5, padx=(7, 10), pady=(20, 0))
        genderCmb = ttk.Combobox(personalInfoGroupBox
                                 , state="readonly"
                                 , width=20
                                 )
        genderCmb['values'] = ('Male'
                               , 'Female'
                               , 'Prefer not to say'
                               )
        genderCmb.grid(row=1, column=6, padx=(7, 10), pady=(20, 0))
        genderCmb.current(0)

        # ======================= ADDRESS INFORMATION ===============================

        addressInfoGroupBox = tk.LabelFrame(mainFrame
                                            , text="Address Information"
                                            , padx=20
                                            , pady=20
                                            , bg="white"
                                            , font=tkFont.Font(family="Arial"
                                                               , size=12
                                                               , weight="bold"
                                                               )
                                            )
        addressInfoGroupBox.pack(padx=20
                                 , pady=(0, 20)
                                 , anchor="w"
                                 )

        street = tk.Label(addressInfoGroupBox
                          , text="Street:"
                          , bg="white"
                          )
        street.grid(row=0, column=1, padx=(0, 10))
        streetEntry = tk.Entry(addressInfoGroupBox
                               , bg="white"
                               , width=25
                               )
        streetEntry.grid(row=0, column=2)

        barangay = tk.Label(addressInfoGroupBox
                            , text="Barangay:"
                            , bg="white"
                            )
        barangay.grid(row=0, column=3, padx=(20, 10))
        barangayEntry = tk.Entry(addressInfoGroupBox
                                 , bg="white"
                                 , width=25
                                 )
        barangayEntry.grid(row=0, column=4)

        city = tk.Label(addressInfoGroupBox
                        , text="City:"
                        , bg="white"
                        )
        city.grid(row=0, column=5, padx=(20, 10))
        cityEntry = tk.Entry(addressInfoGroupBox
                             , bg="white"
                             , width=25
                             )
        cityEntry.grid(row=0, column=6)

        zip = tk.Label(addressInfoGroupBox
                       , text="Zip:"
                       , bg="white"
                       )
        zip.grid(row=1, column=5, padx=(20, 10), pady=(20, 0))
        zipEntry = tk.Entry(addressInfoGroupBox
                            , bg="white"
                            , width=25
                            )
        zipEntry.grid(row=1, column=6, pady=(20, 0))

        # ======================= PROOF OF IDENTITY ===============================

        proofOfIdentityGroupBox = tk.LabelFrame(mainFrame
                                                , text="Proof Of Identity"
                                                , padx=20
                                                , pady=20
                                                , bg="white"
                                                , font=tkFont.Font(family="Arial"
                                                                   , size=12
                                                                   , weight="bold"
                                                                   )
                                                )
        proofOfIdentityGroupBox.pack(padx=20
                                     , pady=(0, 20)
                                     , anchor="w"
                                     )

        proofType = tk.Label(proofOfIdentityGroupBox
                             , text="Type of ID:"
                             , bg="white"
                             )
        proofType.grid(row=0, column=1, padx=(0, 10))
        selectedProofCmb = ttk.Combobox(proofOfIdentityGroupBox
                                        , state="readonly"
                                        , width=30
                                        )
        selectedProofCmb.grid(row=0, column=2, padx=(0, 10))

        # Method of fetching ID from the id_data.json
        def idTypeCmbRefresh():
            # Combo Box Initialization
            idTypeData = idLogic.read_all()
            idTypes = [item for item in idTypeData]
            selectedProofCmb['values'] = idTypes

        idTypeCmbRefresh()

        idNum = tk.Label(proofOfIdentityGroupBox
                         , text="ID Number:"
                         , bg="white"
                         )
        idNum.grid(row=0, column=3, padx=(20, 10))
        idNumEntry = tk.Entry(proofOfIdentityGroupBox
                              , bg="white"
                              , width=25
                              )
        idNumEntry.grid(row=0, column=4)

        # ======================= BOOKING / ROOM ===============================

        def loadRoomsForComboSQL(roomType):
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
                            SELECT RoomID, RoomNumber, Base_Price FROM ROOM
                            WHERE RoomType = ? AND Status = "Available"
                            LIMIT 1
                        """
                cursor.execute(loadRooms, (roomType,))
                room = cursor.fetchone()

                cursor.close()
                conn.close()

                return room

            except Exception as e:
                print("Error connecting to database:", e)
                return None

        def onRoomTypeSelected(e):
            global roomNumber
            global pricePerHour

            selectedRType = roomTypeCmb.get()
            room = loadRoomsForComboSQL(selectedRType)

            if room:

                roomNoEntry.config(state="normal")
                roomNoEntry.delete(0, tk.END)
                roomNoEntry.insert(0, room[1])
                roomNoEntry.config(state="readonly")

                roomIDMap[room[1]] = room[0]
                roomNumber = room[1]
                pricePerHour = room[2]
            else:
                roomNoEntry.config(state="normal")
                roomNoEntry.delete(0, tk.END)
                roomNoEntry.config(state="readonly")

        bookingGroupBox = tk.LabelFrame(mainFrame
                                        , text="Room"
                                        , padx=20
                                        , pady=20
                                        , bg="white"
                                        , font=tkFont.Font(family="Arial"
                                                           , size=12
                                                           , weight="bold"
                                                           )
                                        )
        bookingGroupBox.pack(padx=20
                             , pady=(0, 20)
                             , anchor="w"
                             )

        selectedRoomType = StringVar()
        roomType = tk.Label(bookingGroupBox
                            , text="Room Type:"
                            , bg="white"
                            )
        roomType.grid(row=0, column=1, padx=(0, 10))
        roomTypeCmb = ttk.Combobox(bookingGroupBox
                                   , textvariable=selectedRoomType
                                   , state="readonly"
                                   , width=20
                                   )
        roomTypeCmb.bind("<<ComboboxSelected>>", onRoomTypeSelected)
        roomTypeCmb.grid(row=0, column=2)

        def roomTypeCmbRefresh():
            # Combo Box Initialization
            roomTypeData = logic.read_all()
            roomTypes = [item['name'] for item in roomTypeData]
            roomTypeCmb['values'] = roomTypes

        roomTypeCmbRefresh()

        roomNo = tk.Label(bookingGroupBox
                          , text="Room Number:"
                          , bg="white"
                          )
        roomNo.grid(row=0, column=5, padx=(20, 10))
        roomNoEntry = ttk.Entry(bookingGroupBox
                                , state="readonly"
                                , width=15
                                )
        roomNoEntry.grid(row=0, column=6)

        # ======================= CHECK IN AND OUT ===============================

        checkGroupBox = tk.LabelFrame(mainFrame
                                      , text="Check In and Check Out"
                                      , padx=20
                                      , pady=20
                                      , bg="white"
                                      , font=tkFont.Font(family="Arial"
                                                         , size=12
                                                         , weight="bold"
                                                         )
                                      )
        checkGroupBox.pack(padx=20
                           , pady=(0, 20)
                           , anchor="w"
                           )

        lbl1 = tk.Label(checkGroupBox
                        , text="Select Duration:"
                        , bg="white"
                        )
        lbl1.grid(row=0, column=1)

        lbl2 = tk.Label(checkGroupBox
                        , text="Hour:"
                        , bg="white"
                        )
        lbl2.grid(row=1, column=1, pady=(10, 0))
        hour_cb = ttk.Combobox(checkGroupBox, values=list(range(1, 25)), state="readonly", width=5)
        hour_cb.grid(row=1, column=2, pady=(10, 0))
        lbl3 = tk.Label(checkGroupBox
                        , text="Minutes:"
                        , bg="white"
                        )
        lbl3.grid(row=1, column=3, pady=(10, 0), padx=(10, 0))
        minute_cb = ttk.Combobox(checkGroupBox, values=[0, 15, 30, 45], state="readonly", width=5)
        minute_cb.grid(row=1, column=4, pady=(10, 0), padx=(10, 0))

        hour_cb.bind("<<ComboboxSelected>>", update_booking_info)
        minute_cb.bind("<<ComboboxSelected>>", update_booking_info)

        tk.Label(checkGroupBox, text="Check-In Time:", bg="white").grid(row=2, column=1, pady=(10, 0), padx=(10, 0))
        checkInLabel = tk.Label(checkGroupBox, bg="white")
        checkInLabel.grid(row=2, column=2, pady=(10, 0), padx=(10, 0))

        tk.Label(checkGroupBox, text="Check-Out Time:", bg="white").grid(row=3, column=1, pady=(10, 0), padx=(10, 0))
        checkOutLabel = tk.Label(checkGroupBox, bg="white")
        checkOutLabel.grid(row=3, column=2, pady=(10, 0), padx=(10, 0))

        # ======================= PRICING ===============================

        pricingGroupBox = tk.LabelFrame(mainFrame
                                        , text="Pricing"
                                        , padx=20
                                        , pady=20
                                        , bg="white"
                                        , font=tkFont.Font(family="Arial"
                                                           , size=12
                                                           , weight="bold"
                                                           )
                                        )
        pricingGroupBox.pack(padx=20
                             , pady=(0, 20)
                             , anchor="w"
                             )

        roomPrice = tk.Label(pricingGroupBox
                             , text="Room Base Price: ₱"
                             , bg="white"
                             )
        roomPrice.grid(row=0, column=1, padx=(0, 10))
        roomPriceEntry = tk.Entry(pricingGroupBox
                                  , bg="white"
                                  , width=25
                                  , state="readonly"
                                  , justify="right"
                                  )
        roomPriceEntry.grid(row=0, column=2)

        timePrice = tk.Label(pricingGroupBox
                             , text="Duration (Per Hour/Minute) Subtotal Price: ₱"
                             , bg="white"
                             )
        timePrice.grid(row=2, column=1, padx=(0, 10), pady=(15, 0))
        timePriceEntry = tk.Entry(pricingGroupBox
                                  , bg="white"
                                  , width=25
                                  , state="readonly"
                                  , justify="right"
                                  )
        timePriceEntry.grid(row=2, column=2, pady=(15, 0))

        totalPrice = tk.Label(pricingGroupBox
                              , text="Total Price: ₱"
                              , bg="white"
                              )
        totalPrice.grid(row=3, column=1, padx=(0, 10), pady=(15, 0))
        totalPriceEntry = tk.Entry(pricingGroupBox
                                   , bg="white"
                                   , width=25
                                   , state="readonly"
                                   , justify="right"
                                   )
        totalPriceEntry.grid(row=3, column=2, pady=(15, 0))

        # ======================= CHECK IN BUTTON ===============================

        updateBtn = tk.Button(mainFrame
                              , text="Update"
                              , pady=10
                              , padx=10
                              )
        updateBtn.pack(anchor="w"
                       , padx=(20, 0)
                       , pady=(0, 100)
                       , side="left"
                       )

        deleteBtn = tk.Button(mainFrame
                              , text="Delete"
                              , pady=10
                              , padx=10
                              )
        deleteBtn.pack(anchor="w"
                       , padx=(20, 0)
                       , pady=(0, 100)
                       , side="left"
                       )

        return frame

    # Main System

    # Size of the Window Application
    windowHeight = 720
    windowWidth = 880

    root = tk.Tk()
    root.title("Manage")

    # Updates the Window Size and gives accurate results to screen width and height
    root.update_idletasks()
    centerScreen()
    root.resizable(False, False)

    # Canvas Definition
    canvas = tk.Canvas(root
                       , width=windowWidth
                       , height=windowHeight
                       , bg="white"
                       )
    canvas.pack(fill="both"
                , expand=True
                )

    TOP_FRAME = modelTopFrame()
    MAIN_FRAME = modelMainFrame()

    idm1 = canvas.create_window(windowWidth // 2
                                , 0
                                , window=TOP_FRAME
                                , anchor="n"
                                )
    idm2 = canvas.create_window(windowWidth // 2
                                , 85
                                , window=MAIN_FRAME
                                , anchor="n"
                                )

    root.mainloop()

