# sw_eng_proj1
How to run the project:<br>
Clone/Download repo<br>
Unzip the folder<br>
In terminal/command prompt cd to the repository<br>
Run app.py<br>
It will run locally on your machine.<br>
<br>
Push_data.py:<br>
push_data.py could be run if you would like to update firebase and files<br>
The file pushes filtered data from the hacker news api to firebase<br>
It also creates a file difference_in_jobs.csv<br>
If you choose to run this file YOU MUST manually change the encoding of the csv to UTF-8<br>
This can be done with notepad -> save as -> encoding: UTF-8<br>
running this separately makes the graphs generate quickly for the user in app.py<br>
<br>
App.py:<br>
app.py is a file that connects the data from firebase to plotly graphs<br>
using the Dash framework. <br>
Dash uses only python to create webpages with plotly graphs.<br>
<br>
Graph 4 has a default window of the united states, but if you pan out you can see other parts of the world.<br>
