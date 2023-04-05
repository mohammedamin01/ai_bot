#!/bin/bash
cd /path/to/ai_bot
source venv/bin/activate
python app/scalping.py
deactivate

#Open a terminal or command prompt.
#Type crontab -e and press Enter to open the cronjob configuration file.
#If it is your first time setting up a cronjob, you may be prompted to select an editor. Choose your preferred editor or select the default option.
#Once the editor opens, navigate to the end of the file and add the following line: 0 */8 * * * /path/to/cronjob.sh. Make sure to replace /path/to/cronjob.sh with the actual path to your cronjob file.
#Save and close the file.
#The cronjob should now be active and will run every 8 hours. You can check the status of your cronjobs by typing crontab -l in the terminal.