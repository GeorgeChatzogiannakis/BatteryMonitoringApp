# BatteryMonitoringApp
Ever wonered why your batteries last only so long? <br><br>
Battery manufacturers argue that our charging habits are the main reason our batteries lose their capacity so quickly, and often display a wrong percentage that usually drops rapidly in just a couple of seconds.<br><br>
Although some of the above symptoms are signs of bad battery manufacturing, it is important to adopt better charging habbits to extend the life of our batteries as much as possible and avoid issues like laggy interfaces, overheating and generally reduced performance that could be caused by an 'unhealthy' battery.<br><br>
This app was made to help people monitor the charging process of their batteries, and notify them when to unplug them, keeping both the optimal charge level at all times for them to maintain their battery's longevity and BMS calibrated.<br>

## HOW TO USE:
   Once the app is launched, the user is presented the app's GUI, which displays some parameters of their device, collected by the ``psutil`` library in Python 3. (Device type checks have not been implimented - The app assumes the device has a battery) The user is displayed:
   ### In the top section:
   + The current level of charge of their machine.<br>
   + A suggested percentage to charge to.<br>
   + A slider pre-defined at the optimal percentage position.<br>
   <p>Users are free to change their desired charging percentage -indicated by the position of the slider- at any time before they start the monitoring process, overwriting the initial position of the slider, although this is not suggested.<br>
      
   <b>IMPORTANT: The desired charging percentage is the percentage where the monitoring of the charging is terminated, not where the charging is actually terminated, as this requires to physically unplug the device</b><br>
   <h3>In the middle section:</h3>
      Their desired way of getting notified when the charging reaches the set desired percentage. This section consists of two checkboxes:<br>
      <ul>
         <li> "Play Custom Tune" checkbox</li>
         <li> "Show Popup Notification" checkbox</li>
      </ul><br>
      <b><i>NOTE: To use the 'Play Custom Tune' option, the user must first browse for a supported sound file (.wav/.mp3) to be played when the monitoring detects their desired level of charge has been reached.</i></b><br><br>
      To play a custom tune, the user needs to check the "Play Custom Tune" checkbox after it is enabled.<br>
      <b><i>It is not enough to just browse for a tune to play.</b></i><br>
      The "Show Popup Notification" checkbox will generate a popup to notify the user when the battery reaches the pre-set desired percentage.<br>

   ### In the bottom section:
   <ul>
   <li> A "Browse Tune" button that allows the user to browse for the tune they want their machine to play when the charging reaches their desired pre-set percentage </li>
   <li> A "Selected Tune" label that is set to "None". If a tune is selected to be played when the charging level reaches the pre-set desired percentage, the "None" label will be replaced with the filename of the loaded tune</li>
   <li> An "Enable Monitoring" button that initiates the charging monitoring process </li>
   <li> A "Disable Monitoring" button that stops the monitoring process and resets the interface </li>
   </ul>
