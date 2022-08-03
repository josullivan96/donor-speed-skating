# donor-speed-skating

This program will take exported .csv files of FEC donors from: https://www.fec.gov/data/receipts/?data_type=processed and export a .txt file with a summary of the donors by year:

** 2022 -- Democratic Grassroots Victory Fund $250,000; ActBlue $116,269; ...



## Installation and setup instructions
- Open up a terminal window (`cmd + space` then type "terminal")
- In the terminal install HomeBrew by running: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`
- Install Python with the command: `brew install python`
- Through the terminal, navigate to your desktop with: `cd ~/Desktop`
- Clone this Github repository with: `git clone https://github.com/josullivan96/donor-speed-skating.git`



## Running the program
- Manually download .csv file from FEC site for a single donor: https://www.fec.gov/data/receipts/?data_type=processed
- Drag 1 or more of these .csv files to the `donor-speed-skating` folder on your desktop
- In the terminal, make sure you are in your desktop with: `cd ~/Desktop`
- Run the following command to create summary files for each donor: `python3 donor-list.py`
- You should see .txt files appear in the same folder. Copy and paste them to word doc or wherever