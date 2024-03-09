
# TerraTicket

**Installation instructions**

<ol>
<li>Clone this repository: git clone https://github.com/moored28/SeniorProject </li>

<li>Create a virtual enviroment inside the TerraTicket Folder: <b>python -m venv env </b> </li>
<li>Activate the virtual environment: <b>source env/Scripts/activate</b> for windows or <b>source env/bin/activate</b> for mac</li>

<li>Install all the required dependencies:
<ul><b>pip install django</b></ul>
<ul><b>pip install faker</b> </ul>
<ul><b>pip install pillow</b></ul> </li>
<ul><b>pip install requests</b></ul> </li>


<li>Perform migrations: <b>python manage.py makemigrations</b></li>
<li> Due to dependencies in the models migrate tasks seperately: <b>python manage.py makemigrations tasks</b> </li>
<li>Migrate: <b>python manage.py migrate</b></li>

<li>Generate the fake data: <b>python manage.py shell < tasks/fakedata.py</b> </li>
<li>Optionally create a custom Django admin for access to the admin interface: <b>python manage.py createsuperuser</b> </li>

<li>Run the project: <b>python manage.py runserver</b> </li>
</ol>
