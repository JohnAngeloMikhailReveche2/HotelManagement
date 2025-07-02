import tkinter as tk
from email.policy import default
from tkinter import messagebox as mb, StringVar
from tkinter import ttk
import tkinter.font as tkFont
from tkcalendar import DateEntry

from Pages.dashboard import DASHBOARD_FRAME

# Color HEX Constants
# https://www.color-hex.com/color-palette/1061596
TOP_FRAME_COLOR = "#1a3f73"
DASHBOARD_FRAME_COLOR = "#598dba"
DASHBOARD_BUTTON_COLOR = "#4d6b88"

# CONSTANTS
COLUMN_WIDTH = 100





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
    frame = tk.Frame(canvas
                        , bg= "white"
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

    # ======================= PERSONAL INFORMATION ===============================

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

    nationality = tk.Label(personalInfoGroupBox
                           , text="Nationality:"
                           , bg="white"
                           )
    nationality.grid(row=1, column=3, padx=(7, 10), pady=(20, 0))
    nationalityEntry = tk.Entry(personalInfoGroupBox
                                , bg="white"
                                , width=25
                                )
    nationalityEntry.grid(row=1, column=4, pady=(20, 0))

    selectedGender = StringVar()
    gender = tk.Label(personalInfoGroupBox
                      , text="Gender:"
                      , bg="white"
                      )
    gender.grid(row=1, column=5, padx=(7, 10), pady=(20, 0))
    genderCmb = ttk.Combobox(personalInfoGroupBox
                             , textvariable=selectedGender
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

    selectedProof = StringVar()
    proofType = tk.Label(proofOfIdentityGroupBox
                         , text="Type of ID:"
                         , bg="white"
                         )
    proofType.grid(row=0, column=1, padx=(0, 10))
    selectedProofCmb = ttk.Combobox(proofOfIdentityGroupBox
                                    , textvariable=selectedProof
                                    , state="readonly"
                                    , width=30
                                    )
    selectedProofCmb['values'] = ('Philippine Identification (PhilID) / ePhilID'
                                  , 'Passport'
                                  , 'Unified Multi-purpose Identification (UMID) Card'
                                  , 'Driver''s License'
                                  , 'Professional Regulation Commission (PRC) ID'
                                  , 'Senior Citizen ID'
                                  , 'SSS ID'
                                  , 'BIR (TIN)'
                                  , 'Pag-ibig ID'
                                  , 'Person’s With Disability (PWD) ID'
                                  , 'Solo Parent ID'
                                  , 'Pantawid Pamilya Pilipino Program (4Ps) ID'
                                  , 'Philippine Postal ID'
                                  , 'Phil-health ID'
                                  , 'School ID'
                                  , 'Other valid government-issued IDs'
                                  )
    selectedProofCmb.grid(row=0, column=2)
    selectedProofCmb.current(0)

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

    # ======================= BOOKING ===============================

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
    roomTypeCmb['values'] = ('Standard Room'
                             , 'Deluxe Room'
                             , 'Suite'
                             , 'Junior Suite'
                             , 'Executive Suite'
                             , 'Presidential Suite'
                             , 'Studio Room'
                             , 'Family Room'
                             )
    roomTypeCmb.grid(row=0, column=2)
    roomTypeCmb.current(0)

    selectedBed = StringVar()
    bedType = tk.Label(bookingGroupBox
                       , text="Bed Type:"
                       , bg="white"
                       )
    bedType.grid(row=0, column=3, padx=(20, 10))
    bedTypeCmb = ttk.Combobox(bookingGroupBox
                              , textvariable=selectedBed
                              , state="readonly"
                              , width=25
                              )
    bedTypeCmb['values'] = ('Single Bed'
                            , 'Double Bed'
                            , 'Queen-Sized Bed'
                            , 'King-Sized Bed'
                              'Double-double Bed'
                            )
    bedTypeCmb.grid(row=0, column=4)
    bedTypeCmb.current(0)

    selectedRoom = StringVar()
    roomNo = tk.Label(bookingGroupBox
                      , text="Room Number:"
                      , bg="white"
                      )
    roomNo.grid(row=0, column=5, padx=(20, 10))
    roomNoCmb = ttk.Combobox(bookingGroupBox
                             , textvariable=selectedRoom
                             , state="readonly"
                             , width=5
                             )
    roomNoCmb['values'] = ('1'
                           , '2'
                           , '3'
                           , '4'
                           , '5'
                           )
    roomNoCmb.grid(row=0, column=6)
    roomNoCmb.current(0)

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

    checkInDate = tk.Label(checkGroupBox
                           , text="Check In:"
                           , bg="white"
                           )
    checkInDate.grid(row=0, column=1, padx=(0, 10))
    checkInDateEntry = DateEntry(checkGroupBox
                                 , width=12
                                 , background="white"
                                 , foreground="darkblue"
                                 , borderwidth=2
                                 , state="readonly"
                                 )
    checkInDateEntry.grid(row=0, column=2, padx=(0, 10))

    checkOutDate = tk.Label(checkGroupBox
                            , text="Check Out:"
                            , bg="white"
                            )
    checkOutDate.grid(row=0, column=3, padx=(0, 10))
    checkOutDateEntry = DateEntry(checkGroupBox
                                  , width=12
                                  , background="white"
                                  , foreground="darkblue"
                                  , borderwidth=2
                                  , state="readonly"
                                  )
    checkOutDateEntry.grid(row=0, column=4, padx=(0, 10))

    checkInHour = tk.Label(checkGroupBox
                           , text="Check In Time:"
                           , bg="white"
                           )
    checkInHour.grid(row=1, column=1, padx=(0, 10), pady=(10, 0))

    selectedCheckInHour = tk.StringVar()
    checkInHourSpinBox = tk.Spinbox(checkGroupBox
                                    , from_=1
                                    , to=12
                                    , wrap=True
                                    , textvariable=selectedCheckInHour
                                    , width=5
                                    )
    checkInHourSpinBox.place(x=100, y=32)

    selectedCheckInMin = tk.StringVar()
    selectedCheckInMinSpinBox = tk.Spinbox(checkGroupBox
                                           , from_=0
                                           , to=59
                                           , wrap=True
                                           , format="%02.0f"
                                           , textvariable=selectedCheckInMin
                                           , width=5
                                           )
    selectedCheckInMinSpinBox.place(x=150, y=32)

    selectedAMPM = tk.StringVar()
    ampmComboBox = ttk.Combobox(checkGroupBox
                                , values=["AM", "PM"]
                                , textvariable=selectedAMPM
                                , width=5
                                , state="readonly"
                                )
    ampmComboBox.place(x=200, y=32)
    ampmComboBox.current(0)

    checkOutHour = tk.Label(checkGroupBox
                            , text="Check Out Time:"
                            , bg="white"
                            )
    checkOutHour.grid(row=2, column=1, padx=(0, 10), pady=(10, 0))

    selectedCheckOutHour = tk.StringVar()
    checkOutHourSpinBox = tk.Spinbox(checkGroupBox
                                     , from_=1
                                     , to=12
                                     , wrap=True
                                     , textvariable=selectedCheckOutHour
                                     , width=5
                                     )
    checkOutHourSpinBox.place(x=100, y=63)

    selectedCheckOutMin = tk.StringVar()
    selectedCheckOutMinSpinBox = tk.Spinbox(checkGroupBox
                                            , from_=0
                                            , to=59
                                            , wrap=True
                                            , format="%02.0f"
                                            , textvariable=selectedCheckOutMin
                                            , width=5
                                            )
    selectedCheckOutMinSpinBox.place(x=150, y=63)

    selectedAMPMOut = tk.StringVar()
    outampmComboBox = ttk.Combobox(checkGroupBox
                                   , values=["AM", "PM"]
                                   , textvariable=selectedAMPMOut
                                   , width=5
                                   , state="readonly"
                                   )
    outampmComboBox.place(x=200, y=63)
    outampmComboBox.current(0)

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
                         , text="Room Price: ₱"
                         , bg="white"
                         )
    roomPrice.grid(row=0, column=1, padx=(0, 10))
    roomPriceEntry = tk.Entry(pricingGroupBox
                              , bg="white"
                              , width=15
                              , state="readonly"
                              )
    roomPriceEntry.grid(row=0, column=2)

    bedPrice = tk.Label(pricingGroupBox
                        , text="Bed Price: ₱"
                        , bg="white"
                        )
    bedPrice.grid(row=1, column=1, padx=(0, 10), pady=(15, 0))
    bedPriceEntry = tk.Entry(pricingGroupBox
                             , bg="white"
                             , width=15
                             , state="readonly"
                             )
    bedPriceEntry.grid(row=1, column=2, pady=(15, 0))

    timePrice = tk.Label(pricingGroupBox
                         , text="Time Price: ₱"
                         , bg="white"
                         )
    timePrice.grid(row=2, column=1, padx=(0, 10), pady=(15, 0))
    timePriceEntry = tk.Entry(pricingGroupBox
                              , bg="white"
                              , width=15
                              , state="readonly"
                              )
    timePriceEntry.grid(row=2, column=2, pady=(15, 0))

    totalPrice = tk.Label(pricingGroupBox
                          , text="Total Price: ₱"
                          , bg="white"
                          )
    totalPrice.grid(row=3, column=1, padx=(0, 10), pady=(15, 0))
    totalPriceEntry = tk.Entry(pricingGroupBox
                               , bg="white"
                               , width=15
                               , state="readonly"
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
                   , width = windowWidth
                   , height = windowHeight
                   , bg = "white"
                   )
canvas.pack( fill="both"
             , expand = True
             )


TOP_FRAME = modelTopFrame()
MAIN_FRAME = modelMainFrame()





idm1 = canvas.create_window( windowWidth // 2
                      , 0
                      , window=TOP_FRAME
                      , anchor="n"
                      )
idm2 = canvas.create_window( windowWidth // 2
                      , 85
                      , window=MAIN_FRAME
                      , anchor="n"
                      )














root.mainloop()