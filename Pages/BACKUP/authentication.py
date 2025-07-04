# NOTE: MAKE SURE YOU INSTALLED THE PIL PACKAGE!
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
# NOTE: MAKE SURE YOU INSTALLED THE PIL PACKAGE!
from PIL import Image, ImageTk, ImageEnhance
import os




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
    screenWidth = authRoot.winfo_screenwidth()
    screenHeight = authRoot.winfo_screenheight()

    # Calculate the Center Point
    centerX = int(screenWidth / 2 - windowWidth / 2)
    centerY = int(screenHeight / 2 - windowHeight / 2)

    # Set the geometry based on the Window and Screen Calculations
    authRoot.geometry(f"{windowWidth}x{windowHeight}+{centerX}+{centerY}")

def modelAuthDashboardFrame():

    # Button Initialization
    dashboardFrame = tk.Frame(authCanvas
                        , bg=DASHBOARD_FRAME_COLOR
                        , height=windowHeight
                        , width=250
                        )
    dashboardFrame.pack_propagate(False)

    # ======================= LOGO ===============================
    logoFrame = tk.Frame(dashboardFrame
                          , bg=DASHBOARD_FRAME_COLOR
                          , height=50
                          , width=230
                          )
    logoFrame.pack_propagate(False)
    logoFrame.pack(pady=(100, 0)
                   , padx=(30, 0)
                    )
    logoLabel = tk.Label(logoFrame
                          , text="HOTEL MANAGEMENT"
                          , fg="white"
                          , bg=DASHBOARD_FRAME_COLOR
                          , font=tkFont.Font(family="Arial"
                                             , size=12
                                             , weight="bold"
                                             )
                          )
    logoLabel.pack(anchor="nw")

    # ======================= EMAIL ===============================
    emailFrame = tk.Frame(dashboardFrame
                           , bg=DASHBOARD_FRAME_COLOR
                           , height=50
                           , width=230
                           )
    emailFrame.pack_propagate(False)
    emailFrame.pack(pady=(90, 0)
                     )
    emailLabel = tk.Label(emailFrame
                          , text="Email:"
                          , fg="white"
                          , bg=DASHBOARD_FRAME_COLOR
                          , font=tkFont.Font(family="Arial"
                                             , size=12
                                             , weight="bold"
                                             )
                          )
    emailLabel.pack(anchor="nw")
    emailEntry = tk.Entry(emailFrame
                          , width=25
                          , font=tkFont.Font(family="Arial"
                                             , size=12
                                             )
                          )
    emailEntry.pack(anchor="n")

    # ======================= PASSWORD ===============================

    passwordFrame = tk.Frame(dashboardFrame
                          , bg=DASHBOARD_FRAME_COLOR
                          , height=50
                          , width=230
                          )
    passwordFrame.pack_propagate(False)
    passwordFrame.pack(pady=(20, 0)
                    )
    passwordLabel = tk.Label(passwordFrame
                          , text="Password:"
                          , fg="white"
                          , bg=DASHBOARD_FRAME_COLOR
                          , font=tkFont.Font(family="Arial"
                                             , size=12
                                             , weight="bold"
                                             )
                          )
    passwordLabel.pack(anchor="nw")
    passwordEntry = tk.Entry(passwordFrame
                          , width=25
                          , font=tkFont.Font(family="Arial"
                                             , size=12
                                             )
                          )
    passwordEntry.pack(anchor="n")

    # ======================= LOGIN BTN ===============================

    buttonFrame = tk.Frame(dashboardFrame
                           , bg="white"
                           , height=50
                           , width=250
                           )
    buttonFrame.pack_propagate(False)
    buttonFrame.pack(pady=(40, 0)
                     )

    btnLogIn = tk.Button(buttonFrame
                         , text="LOG IN"
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
    btnLogIn.pack(anchor="n")



    return dashboardFrame

def modelImageFrame():

    # CONSTANTS SETTINGS
    FADE_STEPS = 40 # Increase this for smoother transitions
    DELAY_SHOWIMAGE = 3000
    FADE_DELAY = 50 # mm between fade steps / Control Fade Speed

    # Frame Initialization
    imageFrame = tk.Frame(authCanvas
                        , bg="white"
                        , height=windowHeight
                        , width=1280
                        )
    imageFrame.pack_propagate(False)

    # Get the base directory where authentication.py is
    baseDIR = os.path.dirname(__file__)

    # Build the path towards the image
    imageFolder = os.path.join(baseDIR, "..", "Images")

    # Normalize Path
    imageFolder = os.path.abspath(imageFolder)

    # PLACE IMAGES HERE IF YOU WANT TO ADD MORE
    imagePaths = [
        os.path.join(imageFolder, "hotel1.jfif")
        , os.path.join(imageFolder, "hotel2.jpg")
        , os.path.join(imageFolder, "hotel3.jpg")
        , os.path.join(imageFolder, "hotel4.jpeg")
    ]

    imagePlacementFrame = tk.Frame(imageFrame
                                   , bg="white"
                                   , width=windowWidth
                                   , height=windowHeight
                                   )
    imagePlacementFrame.pack()
    label = tk.Label(imagePlacementFrame)
    label.pack()

    # Mutable Index to track the current image
    imageIndex = [0]

    # Loading and resizing images before slideshow
    loadedImages = [Image.open(path).resize((windowWidth, windowHeight)).convert("RGBA") for path in imagePaths]

    # Current image to blend
    currImage = [loadedImages[0]]

    def showNextImage(step=0):
        nextIndex = (imageIndex[0] + 1) % len(loadedImages)
        nextImage = loadedImages[nextIndex]

        # Blending current and next images
        alpha = step / FADE_STEPS
        blend = Image.blend(currImage[0], nextImage, alpha)
        tkImage = ImageTk.PhotoImage(blend) # Converting the blend to a Tk Image

        label.config(image = tkImage)
        label.image = tkImage # Cache this to be able to use it and load

        if step < FADE_STEPS:
            imagePlacementFrame.after(FADE_DELAY, lambda: showNextImage(step + 1))
        else:
            # After fade completes, update the current image and move to the next image
            imageIndex[0] = nextIndex
            currImage[0] = nextImage
            imagePlacementFrame.after(DELAY_SHOWIMAGE, showNextImage)

    # Start the slideshow
    showNextImage()

    return imageFrame





# MAIN WINDOW

# Size of the Window Application
windowHeight = 720
windowWidth = 1280


# ============================ ENTRY POINT ==============================
authRoot = tk.Tk()
authRoot.title("Hotel Management")

# Updates the Window Size and gives accurate results to screen width and height
authRoot.update_idletasks()
centerScreen()
authRoot.resizable(False, False)



# Canvas Definition
authCanvas = tk.Canvas(authRoot
                   , width = windowWidth
                   , height = windowHeight
                   , bg = "white"
                   )
authCanvas.pack( fill="both"
             , expand = True
             )


# Frames
IMAGE_FRAME = modelImageFrame()
AUTH_DASHBOARD_FRAME = modelAuthDashboardFrame()





# Canvas Initialization for those Frames
authID1 = authCanvas.create_window( 125
                      , 0
                      , window=AUTH_DASHBOARD_FRAME
                      , anchor="n"
                      )

authID2 = authCanvas.create_window( windowWidth // 2
                      , 0
                      , window=IMAGE_FRAME
                      , anchor="n"
                      )










authRoot.mainloop()