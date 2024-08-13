# Mouse actions based on hand gestures
Performing the mouse actions such as left click, right click, zoom, scroll anywhere in your computer/laptop using just the Hand gestures of the user is what this project deal with.

### Tools used
1. Google's MediaPipe framework.
2. PyautoGUI
3. Django
4. Tkinter
5. Pyinstaller

*MediaPipe framework* - MediaPipe is an open-source framework developed by Google for building multimodal (video, audio, etc.) applied machine learning pipelines. We used this framework to detect hands from the video input and get the co-ordinates of a hand. (A palm will be divided into 21 points and we can get the co-ordinates of each point using this framework). So It doesn't recognizes the hand gesture itself, but by applying some math on the co-ordinates that we get, we can determine the hand gesture of the user precisely.

*PyAutoGUI* - In order to perform several mouse actions, we used the PyAutoGUI library of python. It has a cross-platform support. So all the code that we wrote while developing the project was in Linux operating system but we tested them on Windows as well which worked as expected.

*Tkinter* - The handgesture and the mouse actions need to happen on the client side itself inorder to ensure minimum latency and good UI/UX. So we used Tkinter in python to build a desktop app with decent UI which users can use when they need the mouse actions using hand gestures. 

*Django* - It is a popular web development framework in Python. We used it to build a website, where users need to register first and then they can download the desktop application which is responsible for performing mouse actions based on recognized hand gestures. Also users can create their own mapping between the mouse actions and the hand gestures. This will be saved in the website and will be fetched by *API* when using the desktop app.

*PyInstaller* - It is a Python library and command-line tool that converts Python applications into standalone executables, meaning the application can be distributed and run on a target system without requiring the installation of Python or any dependencies. We used this to package our desktop app and made it available for the download on the website.

### Problems faced

I would always looks at the problems that arrise while implemeting a project. So in this project, there are 2 main things, *Hand gesture recognition* and performing *mouse actions* based on the hand gesture that is recognized. So now the potential issues were, 
- If I am designing a website for this, then the mouse actions would be just curtailed to that browser tab only. 
- So just a website wont work. Since I require the mouse action functionality to work everywhere in the laptop (Even though he/she is offline).
- So I have to design a desktop application which when ran, performs mouse actions based on the hand gesture recognized.
 
