
# TerraTicket

**Installation instructions**

<ol>
<li>Clone this repository: git clone https://github.com/moored28/SeniorProject </li>

<li>Create a virtual enviroment inside the TerraTicket Folder: python -m venv env </li>
<li>Activate the virtual environment: source env/Scripts/activate for windows or source env/bin/activate for mac</li>

<li>Install all the required dependencies:
<ul>pip install django</ul>
<ul>pip install faker </ul>
<ul>pip install pillow</ul> </li>

<li>Perform migrations: python manage.py makemigrations</li>
<li>Migrate: python manage.py migrate</li>

<li>Generate the fake data: python manage.py shell < tasks/fakedata.py </li>

<li>Run the project: python manage.py runserver </li>
</ol>
