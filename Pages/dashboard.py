

# System
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

from Classes import ObserverEvent
from Classes.ObserverEvent import Event

from Classes.admin.IDService import IDService
from Classes.admin.RoomTypeService import RoomTypeService

# Pages



# Classes






# Color HEX Constants
# https://www.color-hex.com/color-palette/1061596
TOP_FRAME_COLOR = "#636363"
DASHBOARD_FRAME_COLOR = "#f4f4f4"
DASHBOARD_BUTTON_COLOR = "#C3C7CF"
LOGOUT_BUTTON_COLOR = "#D77A7A"
SIDE_PANEL_TEXT_COLOR = "#8c8c8c"

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

onEventTriggered = Event()
roomTree = None # To fix the loading of roomTree in subscriber
user = None
roomIDMap = {}

def open_dashboard(on_logout_callback):
    global roomTree, historyTree, treeBookingInManage, treeCheckOut

    # ======================== METHODS ===========================

    def loadFilterBookings():
        try:
            # Get the absolute path of this script file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Build the path to the database file
            db_path = os.path.join(script_dir, '..', 'Database', 'hotelManagement.db')
            # Normalize the path (handle ../ correctly)
            db_path = os.path.normpath(db_path)

            conn = sqlite3.connect(db_path)

            cursor = conn.cursor()

            filterValue = filterCmb.get()
            searchTerm = searchEntry.get().strip()

            column_map = {
                'Name': "GUEST.FName || ' ' || COALESCE(GUEST.MName || ' ', '') || GUEST.LName",
                'Contact': 'GUEST.PhoneNumber',
                'ID Proof': 'GUEST.Proof_ID_Type',
                'Room Type': 'ROOM.RoomType',
                'Room Number': 'ROOM.RoomNumber',
                'Check-In': 'BOOKING.CheckInDT',
                'Check-Out': 'BOOKING.CheckOutDT'
            }

            # Base query
            query = """
                    SELECT 
                        GUEST.GuestID,
                        GUEST.FName,
                        GUEST.MName,
                        GUEST.LName,
                        GUEST.PhoneNumber,
                        GUEST.Gender,
                        GUEST.Street,
                        GUEST.Barangay,
                        GUEST.City,
                        GUEST.Zip,
                        GUEST.Proof_ID_Type,
                        GUEST.Proof_ID_Number,
                        ROOM.RoomType,
                        ROOM.RoomNumber,
                        BOOKING.CheckInDT,
                        BOOKING.CheckOutDT,
                        ROUND((julianday(BOOKING.CheckOutDT) - julianday(BOOKING.CheckInDT)) * 24, 2) AS Hour,
                        ROUND(ROOM.Base_Price * (julianday(BOOKING.CheckOutDT) - julianday(BOOKING.CheckInDT)) * 24, 2) AS TotalPrice
                    FROM BOOKING
                    INNER JOIN GUEST ON BOOKING.GuestID = GUEST.GuestID
                    INNER JOIN STAFF ON BOOKING.StaffID = STAFF.StaffID
                    INNER JOIN ROOM ON BOOKING.RoomID = ROOM.RoomID
                    WHERE BOOKING.IsDeleted = 0
                """

            params = []

            if filterValue != "All" and searchTerm:
                query += f" WHERE {column_map[filterValue]} LIKE ?"
                params.append(f"%{searchTerm}%")

            cursor.execute(query, params)
            rows = cursor.fetchall()

            # Clear Tree View
            for item in treeBookingInManage.get_children():
                treeBookingInManage.delete(item)

            # Insert new filtered rows
            for row in rows:
                treeBookingInManage.insert("", tk.END, values=row)

            cursor.close()
            conn.close()

        except Exception as e:
            print("Error connecting to database:", e)
            return None

    # SQL
    #def QueryRoomAvailability():

    def createGuestSQL(fName, mName, lName, gender, phoneNumber, proofID, proofIDNum, street, barangay, zip, city):
        global guestID

        try:
            # Get the absolute path of this script file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Build the path to the database file
            db_path = os.path.join(script_dir, '..', 'Database', 'hotelManagement.db')
            # Normalize the path (handle ../ correctly)
            db_path = os.path.normpath(db_path)

            conn = sqlite3.connect(db_path)

            cursor = conn.cursor()

            createGuest = """
                    INSERT INTO GUEST (FName, MName, LName, Gender, PhoneNumber, Proof_ID_Type, Proof_ID_Number, Street, Barangay, Zip, City, IsDeleted)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(createGuest, (fName, mName, lName, gender, phoneNumber, proofID, proofIDNum, street, barangay, zip, city, 0))
            guestID = cursor.lastrowid
            conn.commit()
            onEventTriggered.notify()

            cursor.close()
            conn.close()



        except Exception as e:
            print("Error connecting to database:", e)
            return None

    def createBookingSQL(selectedRoomID, DTCheckIn, DTCheckOut):
        global roomIDMap

        try:
            # Get the absolute path of this script file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Build the path to the database file
            db_path = os.path.join(script_dir, '..', 'Database', 'hotelManagement.db')
            # Normalize the path (handle ../ correctly)
            db_path = os.path.normpath(db_path)

            conn = sqlite3.connect(db_path)

            cursor = conn.cursor()

            createBookingSQL = """
                    INSERT INTO BOOKING (GuestID, RoomID, StaffID, CheckInDT, CheckOutDT, IsDeleted)
                    VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(createBookingSQL, (guestID, roomIDMap[selectedRoomID], user[0], DTCheckIn, DTCheckOut, 0))
            conn.commit()


            cursor.close()
            conn.close()
            onEventTriggered.notify()

        except Exception as e:
            print("Error connecting to database:", e)
            return None

    def occupyRoomSQL(roomID):
        global roomIDMap

        try:
            # Get the absolute path of this script file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Build the path to the database file
            db_path = os.path.join(script_dir, '..', 'Database', 'hotelManagement.db')
            # Normalize the path (handle ../ correctly)
            db_path = os.path.normpath(db_path)

            conn = sqlite3.connect(db_path)

            cursor = conn.cursor()

            updateRoomSQL = """
                    UPDATE ROOM
                    SET Status = ?
                    WHERE RoomID = ?
                    
            """
            cursor.execute(updateRoomSQL, ("Occupied", roomIDMap[roomID]))
            conn.commit()

            cursor.close()
            conn.close()

            onEventTriggered.notify()

        except Exception as e:
            print("Error connecting to database:", e)
            return None

    def loadBookings(tree):
        try:
            # Get the absolute path of this script file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Build the path to the database file
            db_path = os.path.join(script_dir, '..', 'Database', 'hotelManagement.db')
            # Normalize the path (handle ../ correctly)
            db_path = os.path.normpath(db_path)

            conn = sqlite3.connect(db_path)

            cursor = conn.cursor()

            loadBookingsSQL = """
                    SELECT 
                        BOOKING.BookingID
                        , ROOM.RoomID
                        , GUEST.FName || ' ' || COALESCE(GUEST.MName || ' ', '') || Guest.LName AS GuestFullName
                        , GUEST.PhoneNumber
                        , GUEST.Street || ', ' || COALESCE(GUEST.Barangay || ', ', '') || COALESCE(GUEST.Zip || ', ', '') || GUEST.City AS GuestFullAddress
                        , GUEST.Proof_ID_Type
                        , ROOM.RoomType
                        , ROOM.RoomNumber
                        , BOOKING.CheckInDT
                        , BOOKING.CheckOutDT
                         
                        -- Calculate Total Price
                        , ROUND(ROOM.Base_Price * (julianday(BOOKING.CheckOutDT) - julianday(BOOKING.CheckInDT)) * 24, 2) AS TotalPrice

                    
                    FROM BOOKING
                    INNER JOIN GUEST ON BOOKING.GuestID = GUEST.GuestID
                    INNER JOIN STAFF ON BOOKING.StaffID = STAFF.StaffID
                    INNER JOIN ROOM ON BOOKING.RoomID = ROOM.RoomID 
                    WHERE BOOKING.IsDeleted = 0
            """
            cursor.execute(loadBookingsSQL)
            rows = cursor.fetchall()

            # Clear Previous Data
            for row in tree.get_children():
                tree.delete(row)

            for row in rows:
                tree.insert("", tk.END, values=row)

            cursor.close()
            conn.close()


        except Exception as e:
            print("Error connecting to database:", e)
            return None

    def refreshRoomTree():
        if roomTree:
            loadBookings(roomTree)

    def loadHistory(tree):
        try:
            # Get the absolute path of this script file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Build the path to the database file
            db_path = os.path.join(script_dir, '..', 'Database', 'hotelManagement.db')
            # Normalize the path (handle ../ correctly)
            db_path = os.path.normpath(db_path)

            conn = sqlite3.connect(db_path)

            cursor = conn.cursor()

            loadBookingsSQL = """
                    SELECT
                        BOOKING.BookingID 
                        , GUEST.FName || ' ' || COALESCE(GUEST.MName || ' ', '') || Guest.LName AS GuestFullName
                        , GUEST.PhoneNumber
                        , GUEST.Street || ', ' || COALESCE(GUEST.Barangay || ', ', '') || COALESCE(GUEST.Zip || ', ', '') || GUEST.City AS GuestFullAddress
                        , GUEST.Proof_ID_Type
                        , ROOM.RoomType
                        , ROOM.RoomNumber
                        , BOOKING.CheckInDT
                        , BOOKING.CheckOutDT

                        -- Calculate Total Price
                        , ROUND(ROOM.Base_Price * (julianday(BOOKING.CheckOutDT) - julianday(BOOKING.CheckInDT)) * 24, 2) AS TotalPrice


                    FROM BOOKING
                    INNER JOIN GUEST ON BOOKING.GuestID = GUEST.GuestID
                    INNER JOIN STAFF ON BOOKING.StaffID = STAFF.StaffID
                    INNER JOIN ROOM ON BOOKING.RoomID = ROOM.RoomID
                    WHERE BOOKING.IsDeleted = 1
            """
            cursor.execute(loadBookingsSQL)
            rows = cursor.fetchall()

            # Clear Previous Data
            for row in tree.get_children():
                tree.delete(row)

            for row in rows:
                tree.insert("", tk.END, values=row)

            cursor.close()
            conn.close()

        except Exception as e:
            print("Error connecting to database:", e)
            return None

    def refreshHistoryTree():
        if historyTree:
            loadHistory(historyTree)

    def refreshManageTree():
        if treeBookingInManage:
            loadFilterBookings()

    def refreshCheckOutTree():
        if treeCheckOut:
            loadBookings(treeCheckOut)

    # === Subscribe AFTER ALL refresh methods are defined ===
    onEventTriggered.subscribe(refreshRoomTree)
    onEventTriggered.subscribe(refreshHistoryTree)
    onEventTriggered.subscribe(refreshManageTree)
    onEventTriggered.subscribe(refreshCheckOutTree)

    # === Initial Load of All Trees ===
    refreshRoomTree()

    # System

    def on_dashboard_close():
        # This will stop the mainloop and exit the program
        root.destroy()
        sys.exit()


    # UI Model

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

        # Selected Button Effect Methods
        def onBookingClick():
            BOOKING_FRAME.lift()
            btnBooking.config(bg=SIDE_PANEL_TEXT_COLOR
                              , fg="white"
                              )
            btnManage.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                             )
            btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                              )
            btnCheckOut.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                               )
            btnRoomStat.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                               )

        def onManageClick():
            MANAGE_FRAME.lift()
            btnManage.config(bg=SIDE_PANEL_TEXT_COLOR
                             , fg="white"
                             )
            btnBooking.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                              )
            btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                              )
            btnCheckOut.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                               )
            btnRoomStat.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                               )

        def onHistoryClick():
            HISTORY_FRAME.lift()
            btnHistory.config(bg=SIDE_PANEL_TEXT_COLOR
                             , fg="white"
                              )
            btnBooking.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                              )
            btnManage.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                             )
            btnCheckOut.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                               )
            btnRoomStat.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                               )

        def onCheckOutClick():
            CHECK_OUT_FRAME.lift()
            btnCheckOut.config(bg=SIDE_PANEL_TEXT_COLOR
                             , fg="white"
                               )
            btnBooking.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                              )
            btnManage.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                             )
            btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                              )
            btnRoomStat.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                               )

        def onRoomStatClick():
            ROOM_STATUS_FRAME.lift()
            btnRoomStat.config(bg=SIDE_PANEL_TEXT_COLOR
                             , fg="white"
                               )
            btnBooking.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                              )
            btnManage.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                             )
            btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
                              )
            btnCheckOut.config(bg=DASHBOARD_FRAME_COLOR
                             , fg=SIDE_PANEL_TEXT_COLOR
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
        buttonFrame.pack(pady=(150, 0)
                         )

        btnBooking = tk.Button(buttonFrame
                               , text="Booking"
                               , fg="white"
                               , bg=SIDE_PANEL_TEXT_COLOR
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
                               , command=onBookingClick
                               )
        btnBooking.pack(anchor="n")

        buttonFrame2 = tk.Frame(dashboardFrame
                                , bg=DASHBOARD_FRAME_COLOR
                                , height=50
                                , width=230
                                )
        buttonFrame2.pack_propagate(False)
        buttonFrame2.pack(pady=(20, 0)
                          )

        btnManage = tk.Button(buttonFrame2
                              , text="Manage"
                              , fg=SIDE_PANEL_TEXT_COLOR
                              , bg=DASHBOARD_FRAME_COLOR
                              , height=50
                              , width=230
                              , borderwidth=0
                              , highlightthickness=0
                              , activebackground=SIDE_PANEL_TEXT_COLOR
                              , activeforeground=DASHBOARD_BUTTON_COLOR
                              , relief=tk.FLAT
                              , font=tkFont.Font(family="Arial"
                                                 , size=12
                                                 , weight="bold"
                                                 )
                              , command=onManageClick
                              )
        btnManage.pack(anchor="n")

        buttonFrame3 = tk.Frame(dashboardFrame
                                , bg=DASHBOARD_FRAME_COLOR
                                , height=50
                                , width=230
                                )
        buttonFrame3.pack_propagate(False)
        buttonFrame3.pack(pady=(20, 0)
                          )

        btnHistory = tk.Button(buttonFrame3
                               , text="History"
                               , fg=SIDE_PANEL_TEXT_COLOR
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
                               , command=onHistoryClick
                               )
        btnHistory.pack(anchor="n")

        buttonFrame4 = tk.Frame(dashboardFrame
                                , bg=DASHBOARD_FRAME_COLOR
                                , height=50
                                , width=230
                                )
        buttonFrame4.pack_propagate(False)
        buttonFrame4.pack(pady=(20, 0)
                          )

        btnCheckOut = tk.Button(buttonFrame4
                                , text="Check Out"
                                , fg=SIDE_PANEL_TEXT_COLOR
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
                                , command=onCheckOutClick
                                )
        btnCheckOut.pack(anchor="n")

        buttonFrame6 = tk.Frame(dashboardFrame
                                , bg=DASHBOARD_FRAME_COLOR
                                , height=50
                                , width=230
                                )
        buttonFrame6.pack_propagate(False)
        buttonFrame6.pack(pady=(20, 0)
                          )

        btnRoomStat = tk.Button(buttonFrame6
                                , text="Room Status"
                                , fg=SIDE_PANEL_TEXT_COLOR
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
                                , command=onRoomStatClick
                                )
        btnRoomStat.pack(anchor="n")

        labelFrame = tk.Frame(dashboardFrame
                              , bg=DASHBOARD_FRAME_COLOR
                              , height=70
                              , width=230
                              )
        labelFrame.pack_propagate(False)
        labelFrame.pack(pady=(115, 0)
                        )

        loggedAsLabel = tk.Label(labelFrame
                                 , text=f"Logged In As: \n\n{user[1] + " " + user[3]}"
                                 , bg=DASHBOARD_FRAME_COLOR
                                 , fg=SIDE_PANEL_TEXT_COLOR
                                 , font=tkFont.Font(family="Arial"
                                                    , size=12
                                                    , weight="bold"
                                                    )
                                 )
        loggedAsLabel.pack(anchor="n")

        buttonFrame5 = tk.Frame(dashboardFrame
                                , bg=DASHBOARD_FRAME_COLOR
                                , height=50
                                , width=230
                                )
        buttonFrame5.pack_propagate(False)
        buttonFrame5.pack(pady=(3, 0)
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
                              , command=LogOut
                              )
        btnLogOut.pack(anchor="n")

        return dashboardFrame

    def modelBookingFrame():

        # Methods

        # Register Booking
        def checkInBooking():
            createGuestSQL(fNameEntry.get()
                           , mNameEntry.get()
                           , lNameEntry.get()
                           , genderCmb.get()
                           , phoneNumEntry.get()
                           , selectedProofCmb.get()
                           , idNumEntry.get()
                           , streetEntry.get()
                           , barangayEntry.get()
                           , zipEntry.get()
                           , cityEntry.get()
                           )

            selectedRoom = roomNumber

            createBookingSQL(selectedRoom
                             , checkInGlobal
                             , checkOutGlobal
                             )

            occupyRoomSQL(selectedRoom)


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
                totalTimeHours = hours + (minutes/60)

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


        # Validate Fields
        def validateBookingFields():
            if not fNameEntry.get() or not lNameEntry.get() or not phoneNumEntry.get() or not streetEntry.get() or not barangayEntry.get() or not cityEntry.get() or not zipEntry.get() or not selectedProofCmb.get() or not idNumEntry.get() or not roomTypeCmb.get() or not roomNoEntry.get() or not hour_cb.get() or not minute_cb.get():
                messagebox.showerror("Validation Error", "Please fill in all fields.")
                return

            if not phoneNumEntry.get().isdigit():
                messagebox.showerror("Invalid Input", "Phone number must contain digits only.")
                return

            checkInBooking()
            clearBookingFields()

            onEventTriggered.notify()

            messagebox.showinfo("Success", "Booking is registered successfully!")


        # Clear Fields
        def clearBookingFields():
            global roomIDMap
            global guestID
            global roomNumber
            global pricePerHour
            global durationPrice
            global roomBasePrice
            global checkInGlobal
            global checkOutGlobal

            fNameEntry.delete(0, tk.END)
            mNameEntry.delete(0, tk.END)
            lNameEntry.delete(0, tk.END)
            phoneNumEntry.delete(0, tk.END)
            genderCmb.set('')
            streetEntry.delete(0, tk.END)
            barangayEntry.delete(0, tk.END)
            cityEntry.delete(0, tk.END)
            zipEntry.delete(0, tk.END)
            selectedProofCmb.set('')
            idNumEntry.delete(0, tk.END)
            roomTypeCmb.set('')
            roomNoEntry.config(state="normal")
            roomNoEntry.delete(0, tk.END)
            roomNoEntry.config(state="readonly")
            hour_cb.set('')
            minute_cb.set('')

            totalPriceEntry.config(state="normal")
            timePriceEntry.config(state="normal")
            roomPriceEntry.config(state="normal")
            totalPriceEntry.delete(0, tk.END)
            timePriceEntry.delete(0, tk.END)
            roomPriceEntry.delete(0, tk.END)
            totalPriceEntry.config(state="readonly")
            timePriceEntry.config(state="readonly")
            roomPriceEntry.config(state="readonly")

            roomIDMap = {}
            guestID = 0
            roomNumber = ""
            pricePerHour = 0.0
            durationPrice = 0.0
            roomBasePrice = 0.0
            checkInGlobal = datetime.now()
            checkOutGlobal = datetime.now()



        # Main Methods

        logic = RoomTypeService()
        idLogic = IDService()

        # Note:
        # Scroll_Canvas - is the scrollable area, the actual Canvas widget that can scroll.
        # mainBookingFrame - The contents placed in the canvas, holding widgets. It doesn't scroll itself
        #                     it is moved around by canvas.

        # Main Whole Frame
        bookingFrame = tk.Frame(canvas
                                , bg="white"
                                , height=635
                                , width=1050
                                )
        # This forces the frame to keep the fixed size regardless what's inside of it.
        bookingFrame.pack_propagate(False)

        # A scrollable canvas embedded in the bookingFrame and a scrollbar
        scroll_canvas = tk.Canvas(bookingFrame, width=1050, bg="white")
        scrollbar = tk.Scrollbar(bookingFrame, orient="vertical", command=scroll_canvas.yview)

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
                            , text="Book a Room"
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

        # ======================= PERSONAL INFORMATION ===============================

        personalInfoGroupBox = tk.LabelFrame(mainBookingFrame
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

        addressInfoGroupBox = tk.LabelFrame(mainBookingFrame
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

        proofOfIdentityGroupBox = tk.LabelFrame(mainBookingFrame
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


        bookingGroupBox = tk.LabelFrame(mainBookingFrame
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

        checkGroupBox = tk.LabelFrame(mainBookingFrame
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
        lbl2.grid(row=1, column=1, pady=(10,0))
        hour_cb = ttk.Combobox(checkGroupBox, values=list(range(1, 25)), state="readonly", width=5)
        hour_cb.grid(row=1, column=2, pady=(10,0))
        lbl3 = tk.Label(checkGroupBox
                        , text="Minutes:"
                        , bg="white"
                        )
        lbl3.grid(row=1, column=3, pady=(10, 0), padx=(10,0))
        minute_cb = ttk.Combobox(checkGroupBox, values=[0, 15, 30, 45], state="readonly", width=5)
        minute_cb.grid(row=1, column=4, pady=(10, 0), padx=(10,0))

        hour_cb.bind("<<ComboboxSelected>>", update_booking_info)
        minute_cb.bind("<<ComboboxSelected>>", update_booking_info)

        tk.Label(checkGroupBox, text="Check-In Time:", bg="white").grid(row=2, column=1, pady=(10, 0), padx=(10,0))
        checkInLabel = tk.Label(checkGroupBox, bg="white")
        checkInLabel.grid(row=2, column=2, pady=(10, 0), padx=(10,0))

        tk.Label(checkGroupBox, text="Check-Out Time:", bg="white").grid(row=3, column=1, pady=(10, 0), padx=(10,0))
        checkOutLabel = tk.Label(checkGroupBox, bg="white")
        checkOutLabel.grid(row=3, column=2, pady=(10, 0), padx=(10,0))


        # ======================= PRICING ===============================

        pricingGroupBox = tk.LabelFrame(mainBookingFrame
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

        bookButton = tk.Button(mainBookingFrame
                               , text="Check In"
                               , pady=10
                               , padx=10
                               , command=validateBookingFields
                               )
        bookButton.pack(anchor="w"
                        , padx=(20, 0)
                        , pady=(0, 20)
                        )



        return bookingFrame

    def modelManageFrame():
        global treeBookingInManage, filterCmb, searchEntry


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
                            , text="Manage"
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

        searchEntry = tk.Entry(btnFrame
                               , width=30
                               , borderwidth=3
                               )
        searchEntry.pack(pady=(25, 0), padx=(30, 0), side="left", anchor="w")

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
                               , 'Room Number'
                               , 'Check-In'
                               , 'Check-Out'
                               )
        filterCmb.pack(pady=(25, 0), padx=(15, 0), side="left", anchor="w")
        filterCmb.current(0)

        btnSearch = tk.Button(btnFrame
                              , text="Search"
                              , pady=5
                              , padx=40
                              , command = loadFilterBookings
                              )
        btnSearch.pack(pady=(20, 0), padx=(15, 0), side="left", anchor="w")

        treeContainer = tk.Frame(mainFrame
                                 , width=1000
                                 , height=400
                                 , bg="white"
                                 )
        treeContainer.pack(padx=10, pady=10)
        treeContainer.pack_propagate(False)

        # Treeview Widget
        treeBookingInManage = ttk.Treeview(treeContainer, show="headings", height=17)

        # Columns
        treeBookingInManage['columns'] = ("GuestID"
                           , "FName"
                           , "MName"
                           , "LName"
                           , "PhoneNumber"
                           , "Gender"
                           , "Street"
                           , "Barangay"
                           , "City"
                                          , "Zip"
                                          , "Proof_ID_Type"
                                          , "Proof_ID_Number"
                                          , "RoomType"
                                          , "RoomNumber"
                                          , "CheckInDT"
                                          , "CheckOutDT"
                                          , "Hours"
                                          , "TotalCost"
                           )

        # Formatting Columns
        treeBookingInManage.column("GuestID"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        treeBookingInManage.column("FName"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        treeBookingInManage.column("MName"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        treeBookingInManage.column("LName"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        treeBookingInManage.column("PhoneNumber"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        treeBookingInManage.column("Gender"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        treeBookingInManage.column("Street"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        treeBookingInManage.column("Barangay"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        treeBookingInManage.column("City"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        treeBookingInManage.column("Zip"
                                   , anchor=tk.W
                                   , width=COLUMN_WIDTH
                                   )
        treeBookingInManage.column("Proof_ID_Type"
                                   , anchor=tk.W
                                   , width=COLUMN_WIDTH
                                   )
        treeBookingInManage.column("Proof_ID_Number"
                                   , anchor=tk.W
                                   , width=COLUMN_WIDTH
                                   )
        treeBookingInManage.column("RoomType"
                                   , anchor=tk.W
                                   , width=COLUMN_WIDTH
                                   )
        treeBookingInManage.column("RoomNumber"
                                   , anchor=tk.W
                                   , width=COLUMN_WIDTH
                                   )
        treeBookingInManage.column("CheckInDT"
                                   , anchor=tk.W
                                   , width=COLUMN_WIDTH
                                   )
        treeBookingInManage.column("CheckOutDT"
                                   , anchor=tk.W
                                   , width=COLUMN_WIDTH
                                   )
        treeBookingInManage.column("Hours"
                                   , anchor=tk.W
                                   , width=COLUMN_WIDTH
                                   )
        treeBookingInManage.column("TotalCost"
                                   , anchor=tk.W
                                   , width=COLUMN_WIDTH
                                   )

        # Create Headings
        treeBookingInManage.heading("GuestID"
                     , text="Guest ID"
                     , anchor=tk.W
                     )
        treeBookingInManage.heading("FName"
                     , text="FName"
                     , anchor=tk.W
                     )
        treeBookingInManage.heading("MName"
                     , text="MName"
                     , anchor=tk.W
                     )
        treeBookingInManage.heading("LName"
                     , text="LName"
                     , anchor=tk.W
                     )
        treeBookingInManage.heading("PhoneNumber"
                     , text="Phone Number"
                     , anchor=tk.W
                     )
        treeBookingInManage.heading("Gender"
                     , text="Room Number"
                     , anchor=tk.W
                     )
        treeBookingInManage.heading("Street"
                     , text="Street"
                     , anchor=tk.W
                     )
        treeBookingInManage.heading("Barangay"
                     , text="Barangay"
                     , anchor=tk.W
                     )
        treeBookingInManage.heading("City"
                     , text="City"
                     , anchor=tk.W
                     )
        treeBookingInManage.heading("Zip"
                                    , text="Zip"
                                    , anchor=tk.W
                                    )
        treeBookingInManage.heading("Proof_ID_Type"
                                    , text="Proof_ID_Type"
                                    , anchor=tk.W
                                    )
        treeBookingInManage.heading("Proof_ID_Number"
                                    , text="Proof_ID_Number"
                                    , anchor=tk.W
                                    )
        treeBookingInManage.heading("RoomType"
                                    , text="RoomType"
                                    , anchor=tk.W
                                    )
        treeBookingInManage.heading("RoomNumber"
                                    , text="RoomNumber"
                                    , anchor=tk.W
                                    )
        treeBookingInManage.heading("CheckInDT"
                                    , text="CheckIn Date Time"
                                    , anchor=tk.W
                                    )
        treeBookingInManage.heading("CheckOutDT"
                                    , text="CheckOut Date Time"
                                    , anchor=tk.W
                                    )
        treeBookingInManage.heading("Hours"
                                    , text="Hours"
                                    , anchor=tk.W
                                    )
        treeBookingInManage.heading("TotalCost"
                                    , text="TotalCost"
                                    , anchor=tk.W
                                    )


        # Horizontal Scrollbar
        scrollbar = ttk.Scrollbar(treeContainer
                                  , orient="horizontal"
                                  , command=treeBookingInManage.xview
                                  )
        treeBookingInManage.configure(xscrollcommand=scrollbar.set)

        # Pack
        treeBookingInManage.pack(pady=(10, 0), padx=(10, 0), anchor="nw")
        scrollbar.pack(side="bottom", fill="x")

        def openDetailWindow(e):
            selectedItem = treeBookingInManage.focus()
            if not selectedItem:
                return
            rowData = treeBookingInManage.item(selectedItem, 'values')
            from modify import openDetailWindow
            openDetailWindow(rowData)

        treeBookingInManage.bind("<Double-1>", openDetailWindow)

        loadFilterBookings()
        treeBookingInManage = treeBookingInManage  # or assign your actual tree here

        refreshManageTree()  # ✅ Now it is safe to call this
        return frame

    def modelHistoryFrame():
        global historyTree

        def loadFilterHistory():
            try:
                # Get the absolute path of this script file
                script_dir = os.path.dirname(os.path.abspath(__file__))
                # Build the path to the database file
                db_path = os.path.join(script_dir, '..', 'Database', 'hotelManagement.db')
                # Normalize the path (handle ../ correctly)
                db_path = os.path.normpath(db_path)

                conn = sqlite3.connect(db_path)

                cursor = conn.cursor()

                filterValue = filterCmb.get()
                searchTerm = searchEntry.get().strip()

                column_map = {
                    'Name': "GUEST.FName || ' ' || COALESCE(GUEST.MName || ' ', '') || GUEST.LName",
                    'Contact': 'GUEST.PhoneNumber',
                    'ID Proof': 'GUEST.Proof_ID_Type',
                    'Room Type': 'ROOM.RoomType',
                    'Room Number': 'ROOM.RoomNumber',
                    'Check-In': 'BOOKING.CheckInDT',
                    'Check-Out': 'BOOKING.CheckOutDT'
                }

                # Base query
                query = """
                    SELECT
                        BOOKING.BookingID 
                        , GUEST.FName || ' ' || COALESCE(GUEST.MName || ' ', '') || Guest.LName AS GuestFullName
                        , GUEST.PhoneNumber
                        , GUEST.Street || ', ' || COALESCE(GUEST.Barangay || ', ', '') || COALESCE(GUEST.Zip || ', ', '') || GUEST.City AS GuestFullAddress
                        , GUEST.Proof_ID_Type
                        , ROOM.RoomType
                        , ROOM.RoomNumber
                        , BOOKING.CheckInDT
                        , BOOKING.CheckOutDT

                        -- Calculate Total Price
                        , ROUND(ROOM.Base_Price * (julianday(BOOKING.CheckOutDT) - julianday(BOOKING.CheckInDT)) * 24, 2) AS TotalPrice


                    FROM BOOKING
                    INNER JOIN GUEST ON BOOKING.GuestID = GUEST.GuestID
                    INNER JOIN STAFF ON BOOKING.StaffID = STAFF.StaffID
                    INNER JOIN ROOM ON BOOKING.RoomID = ROOM.RoomID
   
                    """


                params = []

                if filterValue != "All" and searchTerm:
                    query += f" WHERE {column_map[filterValue]} LIKE ?"
                    params.append(f"%{searchTerm}%")

                query += f" AND BOOKING.IsDeleted = 1"

                cursor.execute(query, params)
                rows = cursor.fetchall()

                # Clear Tree View
                for item in tree.get_children():
                    tree.delete(item)

                # Insert new filtered rows
                for row in rows:
                    tree.insert("", tk.END, values=row)

                cursor.close()
                conn.close()

            except Exception as e:
                print("Error connecting to database:", e)
                return None
        # Note: HIHI
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
                              , command= loadFilterHistory
                              )
        btnSearch.pack(pady=(20, 0), padx=(15, 0), side="left", anchor="w")

        btnReset = tk.Button(btnFrame
                             , text="Reset"
                             , pady=5
                             , padx=40
                             , command= lambda: loadHistory(tree)
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
        tree['columns'] = ("GuestID"
                           , "Name"
                           , "Contact"
                           , "Address"
                           , "IDProof"
                           , "RoomType"
                           , "RoomNumber"
                           , "Check-In"
                           , "Check-Out"
                           , "TotalPrice"
                           )

        # Formatting Columns
        tree.column("GuestID"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
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
        tree.column("IDProof"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        tree.column("RoomType"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        tree.column("RoomNumber"
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
        tree.column("TotalPrice"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )


        # Create Headings
        tree.heading("GuestID"
                     , text="Guest ID"
                     , anchor=tk.W
                     )
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
        tree.heading("IDProof"
                     , text="ID Proof"
                     , anchor=tk.W
                     )
        tree.heading("RoomType"
                     , text="Room Type"
                     , anchor=tk.W
                     )
        tree.heading("RoomNumber"
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
        tree.heading("TotalPrice"
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
        tree.pack(pady=(10, 0), padx=(10, 0), anchor="nw")
        scrollbar.pack(side="bottom", fill="x")

        loadHistory(tree)
        historyTree = tree  # ✅ This gives refreshHistoryTree() access to the tree
        refreshHistoryTree()

        return frame

    def modelCheckOutFrame():
        global treeCheckOut

        def onCheckOut():
            selectedItem = tree.focus()
            if not selectedItem:
                return

            values = tree.item(selectedItem, 'values')

            if values:
                availableRoomSQL(values[1])
                checkOut(values[0])
                loadBookings(tree)

                onEventTriggered.notify()


                nameEntry.config(state="normal")
                nameEntry.delete(0, tk.END)
                nameEntry.config(state="readonly")

                roomNoEntry.config(state="normal")
                roomNoEntry.delete(0, tk.END)
                roomNoEntry.config(state="readonly")

                checkOutDateEntry.config(state="normal")
                checkOutDateEntry.delete(0, tk.END)
                checkOutDateEntry.config(state="readonly")

        def checkOut(bookingID):
            try:
                # Get the absolute path of this script file
                script_dir = os.path.dirname(os.path.abspath(__file__))
                # Build the path to the database file
                db_path = os.path.join(script_dir, '..', 'Database', 'hotelManagement.db')
                # Normalize the path (handle ../ correctly)
                db_path = os.path.normpath(db_path)

                conn = sqlite3.connect(db_path)

                cursor = conn.cursor()

                updateRoomSQL = """
                               UPDATE BOOKING
                               SET IsDeleted = ?
                               WHERE BookingID = ?
                       """
                cursor.execute(updateRoomSQL, (1, bookingID))
                conn.commit()

                cursor.close()
                conn.close()

            except Exception as e:
                print("Error connecting to database:", e)
                return None

        def availableRoomSQL(roomID):

            try:
                # Get the absolute path of this script file
                script_dir = os.path.dirname(os.path.abspath(__file__))
                # Build the path to the database file
                db_path = os.path.join(script_dir, '..', 'Database', 'hotelManagement.db')
                # Normalize the path (handle ../ correctly)
                db_path = os.path.normpath(db_path)

                conn = sqlite3.connect(db_path)

                cursor = conn.cursor()

                updateRoomSQL = """
                        UPDATE ROOM
                        SET Status = ?
                        WHERE RoomID = ?

                """
                cursor.execute(updateRoomSQL, ("Available", roomID))
                conn.commit()

                cursor.close()
                conn.close()

            except Exception as e:
                print("Error connecting to database:", e)
                return None

        def itemOnSelect(e):
            selectedItem = tree.focus()
            if not selectedItem:
                return

            values = tree.item(selectedItem, 'values')

            if values:
                nameEntry.config(state="normal")
                nameEntry.delete(0, tk.END)
                nameEntry.insert(0, values[0])
                nameEntry.config(state="readonly")

                roomNoEntry.config(state="normal")
                roomNoEntry.delete(0, tk.END)
                roomNoEntry.insert(0, values[4])
                roomNoEntry.config(state="readonly")

                checkOutDateEntry.config(state="normal")
                checkOutDateEntry.delete(0, tk.END)
                checkOutDateEntry.insert(0, values[6])
                checkOutDateEntry.config(state="readonly")



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
                            , text="Check Out a Booking"
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

        nameEntry = tk.Entry(btnFrame
                             , width=20
                             , borderwidth=3
                             , state="readonly"
                             )
        nameEntry.pack(pady=(25, 0), padx=(20, 0), side="left", anchor="w")

        roomNoEntry = tk.Entry(btnFrame
                               , width=20
                               , borderwidth=3
                               , state="readonly"
                               )
        roomNoEntry.pack(pady=(25, 0), padx=(10, 0), side="left", anchor="w")

        checkOutDateEntry = tk.Entry(btnFrame
                                     , width=20
                                     , borderwidth=3
                                     , state="readonly"
                                     )
        checkOutDateEntry.pack(pady=(25, 0), padx=(10, 0), side="left", anchor="w")

        btnCheckOut = tk.Button(btnFrame
                              , text="Check Out"
                              , pady=5
                              , padx=40
                              , command=onCheckOut
                              )
        btnCheckOut.pack(pady=(20, 0), padx=(15, 0), side="left", anchor="w")

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
        tree['columns'] = ("BookingID"
                           , "RoomID"
                           , "Name"
                           , "Contact"
                           , "Address"
                           , "ProofID"
                           , "RoomType"
                           , "RoomNumber"
                           , "CheckIn"
                           , "CheckOut"
                           , "TotalPrice"
                           )

        # Formatting Columns
        tree.column("BookingID"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        tree.column("RoomID"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
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
        tree.column("ProofID"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        tree.column("RoomType"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        tree.column("RoomNumber"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        tree.column("CheckIn"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        tree.column("CheckOut"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )
        tree.column("TotalPrice"
                    , anchor=tk.W
                    , width=COLUMN_WIDTH
                    )


        # Create Headings
        tree.heading("BookingID"
                     , text="Booking ID"
                     , anchor=tk.W
                     )
        tree.heading("RoomID"
                     , text="Room ID"
                     , anchor=tk.W
                     )
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
        tree.heading("ProofID"
                     , text="Proof ID"
                     , anchor=tk.W
                     )
        tree.heading("RoomType"
                     , text="Room Type"
                     , anchor=tk.W
                     )
        tree.heading("RoomNumber"
                     , text="Room Number"
                     , anchor=tk.W
                     )
        tree.heading("CheckIn"
                     , text="Check In"
                     , anchor=tk.W
                     )
        tree.heading("CheckOut"
                     , text="Check Out"
                     , anchor=tk.W
                     )
        tree.heading("TotalPrice"
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
        tree.pack(pady=(10, 0), padx=(10, 0), anchor="nw")
        scrollbar.pack(side="bottom", fill="x")

        treeCheckOut = tree

        loadBookings(tree)
        refreshCheckOutTree()

        tree.bind("<<TreeviewSelect>>", itemOnSelect)

        return frame

    def modelRoomStatusFrame():

        def filterResults(tree, filterBy, searchTerm):
            try:
                # Get the absolute path of this script file
                script_dir = os.path.dirname(os.path.abspath(__file__))
                # Build the path to the database file
                db_path = os.path.join(script_dir, '..', 'Database', 'hotelManagement.db')
                # Normalize the path (handle ../ correctly)
                db_path = os.path.normpath(db_path)

                column_map = {
                    "Room Type": "RoomType",
                    "Bed Type": "BedType",
                    "Status": "Status"
                }

                selectedFilter = filterBy.get()
                keyword = searchTerm.get().strip()

                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                filterSql = """
                        SELECT RoomID, RoomNumber, RoomType, BedType, RoomCapacity, Status
                        FROM ROOM
                """
                params = []

                if selectedFilter == "All" and keyword:
                    # Search all three fields
                    filterSql += " WHERE RoomType LIKE ? OR BedType LIKE ? OR Status LIKE ?"
                    likeKeyword = f"%{keyword}%"
                    params.extend([likeKeyword, likeKeyword, likeKeyword])
                elif selectedFilter in column_map and keyword:
                    column = column_map[selectedFilter]
                    filterSql += f" WHERE {column} LIKE ?"
                    params.append(f"%{keyword}%")

                cursor.execute(filterSql, params)
                rows = cursor.fetchall()

                # Clear treeview and insert results
                for item in tree.get_children():
                    tree.delete(item)

                for idx, row in enumerate(rows):
                    tree.insert('', 'end', iid=str(idx), values=row)

                # Close
                cursor.close()
                conn.close()

            except Exception as e:
                print("Error connecting to database:", e)
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

        searchTerm = StringVar()
        searchEntry = tk.Entry(btnFrame
                               , width=30
                               , borderwidth=3
                               , textvariable = searchTerm
                               )
        searchEntry.pack(pady=(25, 0), padx=(10, 0), side="left", anchor="w")

        btnSearch = tk.Button(btnFrame
                              , text="Search"
                              , pady=5
                              , padx=40
                              , command=lambda: filterResults(roomTree, filterCmb, searchEntry)
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
        roomTree['columns'] = ("Room ID"
                               , "Room Number"
                               , "Room Type"
                               , "Bed Type"
                               , "Room Capacity"
                               , "Status"
                               )

        # Formatting Columns
        roomTree.column("Room Number"
                        , anchor=tk.W
                        , width=COLUMN_WIDTH
                        )
        roomTree.column("Room ID"
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
        roomTree.column("Room Capacity"
                        , anchor=tk.W
                        , width=COLUMN_WIDTH
                        )
        roomTree.column("Status"
                        , anchor=tk.W
                        , width=COLUMN_WIDTH
                        )

        # Headings
        roomTree.heading("Room ID", text="Room ID")
        roomTree.heading("Room Type", text="Room Type")
        roomTree.heading("Bed Type", text="Bed Type")
        roomTree.heading("Room Capacity", text="Room Capacity")
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

        # TREE VIEW METHODS ===========================================

        def loadRoomData():
            # Clear Existing Rows to avoid duplicates
            for item in roomTree.get_children():
                roomTree.delete(item)

            # Load new data
            loadRoomSQL(roomTree)

        # TREE VIEW METHODS ===========================================

        # Load the Room Data from Database
        loadRoomData()


        return frame

    # Authentication

    def readUserAuthenticate(userData):
        try:
            # Get the absolute path of this script file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Build the path to the database file
            db_path = os.path.join(script_dir, '..', 'Database', 'hotelManagement.db')
            # Normalize the path (handle ../ correctly)
            db_path = os.path.normpath(db_path)

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            query = """
                SELECT * FROM STAFF
                WHERE StaffID = ?
            """

            userID = int(userData.get('id'))

            cursor.execute(query, (userID,))

            cachedUser = cursor.fetchone()

            cursor.close()
            conn.close()

            if cachedUser:
                return True, cachedUser
            else:
                return False, None

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return False, None

    def LogOut():
        root.destroy()  # close the dashboard
        on_logout_callback()  # call the callback to reopen login window

    # ======================== METHODS ===========================

    # Size of the Window Application
    windowHeight = 720
    windowWidth = 1280

    # ============================ ENTRY POINT ==============================

    dataFile = "userData.json"

    # Check if the file exists
    if os.path.exists(dataFile):
        # Read and parse the data
        with open(dataFile, "r") as f:
            cachedUserData = json.load(f)

        # Delete the file right after loading
        os.remove(dataFile)

    success, user = readUserAuthenticate(cachedUserData)

    root = tk.Tk()
    root.title("Hotel Management - 2")
    # Updates the Window Size and g,.mm ives accurate results to screen width and height
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

    # Define Model Frames and their Elements
    DASHBOARD_FRAME = modelDashboardFrame()
    TOP_FRAME = modelTopFrame()
    MANAGE_FRAME = modelManageFrame()
    BOOKING_FRAME = modelBookingFrame()
    HISTORY_FRAME = modelHistoryFrame()
    CHECK_OUT_FRAME = modelCheckOutFrame()
    ROOM_STATUS_FRAME = modelRoomStatusFrame()

    # Initialize Frames or Canvas related UI Elements
    id1 = canvas.create_window(windowWidth // 2
                               , 0
                               , window=TOP_FRAME
                               , anchor="n"
                               )

    id2 = canvas.create_window(0
                               , windowHeight // 2
                               , window=DASHBOARD_FRAME
                               , anchor="w"
                               )

    id3 = canvas.create_window(755
                               , windowHeight // 2 + 42
                               , window=BOOKING_FRAME
                               )

    id4 = canvas.create_window(755
                               , windowHeight // 2 + 42
                               , window=MANAGE_FRAME
                               )

    id5 = canvas.create_window(755
                               , windowHeight // 2 + 42
                               , window=HISTORY_FRAME
                               )

    id6 = canvas.create_window(755
                               , windowHeight // 2 + 42
                               , window=CHECK_OUT_FRAME
                               )

    id7 = canvas.create_window(755
                               , windowHeight // 2 + 42
                               , window=ROOM_STATUS_FRAME
                               )

    # Canvas Configurations
    canvas.itemconfigure(id3
                         , state='normal'
                         )
    BOOKING_FRAME.lift()


    root.protocol("WM_DELETE_WINDOW", on_dashboard_close)
    # Application Loop
    root.mainloop()

