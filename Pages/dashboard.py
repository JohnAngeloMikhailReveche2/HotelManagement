

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

from Classes.admin.IDService import IDService
from Classes.admin.RoomTypeService import RoomTypeService

# Pages



# Classes






# Color HEX Constants
# https://www.color-hex.com/color-palette/1061596
TOP_FRAME_COLOR = "#1a3f73"
DASHBOARD_FRAME_COLOR = "#598dba"
DASHBOARD_BUTTON_COLOR = "#4d6b88"
LOGOUT_BUTTON_COLOR = "#407099"

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



def open_dashboard(on_logout_callback):
    root = tk.Toplevel

    # ======================== METHODS ===========================

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

        except Exception as e:
            print("Error connecting to database:", e)
            return None











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
            btnBooking.config(bg="white"
                              , fg=DASHBOARD_BUTTON_COLOR
                              )
            btnManage.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="white"
                             )
            btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                              , fg="white"
                              )
            btnCheckOut.config(bg=DASHBOARD_FRAME_COLOR
                               , fg="white"
                               )
            btnRoomStat.config(bg=DASHBOARD_FRAME_COLOR
                               , fg="white"
                               )

        def onManageClick():
            MANAGE_FRAME.lift()
            btnManage.config(bg="white"
                             , fg=DASHBOARD_BUTTON_COLOR
                             )
            btnBooking.config(bg=DASHBOARD_FRAME_COLOR
                              , fg="white"
                              )
            btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                              , fg="white"
                              )
            btnCheckOut.config(bg=DASHBOARD_FRAME_COLOR
                               , fg="white"
                               )
            btnRoomStat.config(bg=DASHBOARD_FRAME_COLOR
                               , fg="white"
                               )

        def onHistoryClick():
            HISTORY_FRAME.lift()
            btnHistory.config(bg="white"
                              , fg=DASHBOARD_BUTTON_COLOR
                              )
            btnBooking.config(bg=DASHBOARD_FRAME_COLOR
                              , fg="white"
                              )
            btnManage.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="white"
                             )
            btnCheckOut.config(bg=DASHBOARD_FRAME_COLOR
                               , fg="white"
                               )
            btnRoomStat.config(bg=DASHBOARD_FRAME_COLOR
                               , fg="white"
                               )

        def onCheckOutClick():
            CHECK_OUT_FRAME.lift()
            btnCheckOut.config(bg="white"
                               , fg=DASHBOARD_BUTTON_COLOR
                               )
            btnBooking.config(bg=DASHBOARD_FRAME_COLOR
                              , fg="white"
                              )
            btnManage.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="white"
                             )
            btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                              , fg="white"
                              )
            btnRoomStat.config(bg=DASHBOARD_FRAME_COLOR
                               , fg="white"
                               )

        def onRoomStatClick():
            ROOM_STATUS_FRAME.lift()
            btnRoomStat.config(bg="white"
                               , fg=DASHBOARD_BUTTON_COLOR
                               )
            btnBooking.config(bg=DASHBOARD_FRAME_COLOR
                              , fg="white"
                              )
            btnManage.config(bg=DASHBOARD_FRAME_COLOR
                             , fg="white"
                             )
            btnHistory.config(bg=DASHBOARD_FRAME_COLOR
                              , fg="white"
                              )
            btnCheckOut.config(bg=DASHBOARD_FRAME_COLOR
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
        buttonFrame.pack(pady=(150, 0)
                         )

        btnBooking = tk.Button(buttonFrame
                               , text="Booking"
                               , fg=DASHBOARD_BUTTON_COLOR
                               , bg="white"
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
                                 , fg="white"
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

            checkInBooking()
            clearBookingFields()
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
                               , 'Bed Type'
                               , 'Room Number'
                               , 'Check-In'
                               , 'Check-Out'
                               , 'Rent Time'
                               )
        filterCmb.pack(pady=(25, 0), padx=(15, 0), side="left", anchor="w")
        filterCmb.current(0)

        btnSearch = tk.Button(btnFrame
                              , text="Search"
                              , pady=5
                              , padx=40
                              )
        btnSearch.pack(pady=(20, 0), padx=(15, 0), side="left", anchor="w")

        btnDelete = tk.Button(btnFrame
                              , text="Delete"
                              , pady=5
                              , padx=40
                              )
        btnDelete.pack(pady=(20, 0), padx=(15, 0), side="left", anchor="w")

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
        tree.pack(pady=(10, 0), padx=(10, 0), anchor="nw")
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
                               , 'Rent Time'
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
        tree.pack(pady=(10, 0), padx=(10, 0), anchor="nw")
        scrollbar.pack(side="bottom", fill="x")

        return frame

    def modelCheckOutFrame():

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

        checkoutTimeEntry = tk.Entry(btnFrame
                                     , width=20
                                     , borderwidth=3
                                     , state="readonly"
                                     )
        checkoutTimeEntry.pack(pady=(25, 0), padx=(10, 0), side="left", anchor="w")

        btnSearch = tk.Button(btnFrame
                              , text="Check Out"
                              , pady=5
                              , padx=40
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
        tree.pack(pady=(10, 0), padx=(10, 0), anchor="nw")
        scrollbar.pack(side="bottom", fill="x")

        return frame

    def modelRoomStatusFrame():

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

