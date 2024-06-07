***This converter has been developed on ubuntu linux, so the setup is according to ubuntu***

1. Install tkinter
sudo apt install python3-tk

2. Install additional libraries
sudo apt-get install xvfb
sudo apt install qtwayland5 
sudo apt install qt6-wayland

3. Export Environmental variable
export QT_QPA_PLATFORM=xcb

4. Create virtual environemnt
python3 -m venv venv

5. Actvate virtual environment
source venv/bin/activate

6. Install requirements
pip3 install -r requirements.txt

7. Get oda file converter .deb file from this link-
https://www.opendesign.com/guestfiles/oda_file_converter

8. Install deb file
cd Downloads
sudo dpkg -i <deb file name>


9. Run the convert script with command-
python3 convert.py


UI Instructions
1. An interface will pop up
2. You will need to specify your .dwg file by clicking on 1st browse button
3. After selecting file you can see location of file on UI
4. Now specify the location where you want your output files by clicking on next browse button
5. After selecting folder location you can see location on UI
6. Click on convert button to start the process
7. After process is finished, you can see output files at the output location, this converter will produce 4 output files- .shp, .shx, .dbf, .cpg

