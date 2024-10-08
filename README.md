# Aurora Alert

Aurora Alert is a Python application designed to monitor geomagnetic activity and alert users of potential aurora visibility based on the Kp index. The application checks the aurora forecast periodically from the Soft Serve News website (https://softservenews.com/) and sends notifications during optimal viewing times, ensuring users don't miss out on nature's spectacular light show.

## Features

- **Real-time Aurora Monitoring:** Continuously checks aurora forecasts to detect high geomagnetic activity.
- **Email Notifications:** Sends email alerts when the Kp index reaches a threshold that suggests visibility of the aurora borealis.
- **Customizable Alert Threshold:** Users can set the Kp index threshold for alerts based on their local visibility conditions.
- **Automated Timing:** Only sends alerts during nighttime hours, adjusting for local sunrise and sunset times to ensure alerts are relevant.
- **24/7 Monitoring with Task Scheduler**: Set up Task Scheduler on Windows to run the script continuously in the background.
