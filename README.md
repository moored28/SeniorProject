
# TerraTicket

**Installation instructions**

<ol>
<li>Clone this repository: git clone https://github.com/moored28/SeniorProject </li>

<li>Create a virtual enviroment inside the TerraTicket Folder: <b>python -m venv env </b> </li>
<li>Activate the virtual environment: <b>source env/Scripts/activate</b> for windows or <b>source env/bin/activate</b> for mac</li>

<li>Install all the required dependencies:
<ul><b>pip install django</b></ul>
<ul><b>pip install faker</b> </ul>
<ul><b>pip install pillow</b></ul> 
<ul><b>pip install requests</b></ul> 
<ul><b>pip install googlemaps</b></ul></li>


<li>Perform migrations: <b>python manage.py makemigrations</b></li>
<li> Due to dependencies in the models migrate tasks seperately: <b>python manage.py makemigrations tasks</b> </li>
<li>Migrate: <b>python manage.py migrate</b></li>

<ol>
    <li><b>Create a Google Cloud Platform Project:</b><br>
        - Go to the <a href="https://console.cloud.google.com/">Google Cloud Platform Console</a>.<br>
        - Create a new project or select an existing one.
    </li>
    <li><b>Enable the Required API:</b><br>
        - Under API Library select "Maps Javascript API" and Enable it
    </li>
    <li><b>Create API Key:</b><br>
        - Go to the "Credentials" tab in the left sidebar menu.<br>
        - Click on the "Create credentials" dropdown and select "API key".<br>
        - Google will generate an API key for you. Copy it and keep it secure.
    </li>
    <li><b>Store API Key as Environment Variable:</b><br>
        - Add <code>GOOGLE_MAPS_API_KEY=your_api_key_here</code> to the pyvenv.cfg file
    </li>
    <li><b>Load API Key in Django Settings:</b><br>
        - In your Django settings djangoproject/settings.py, use <code>os.environ.get('GOOGLE_MAPS_API_KEY')</code> to access the API key from the environment variable.
    </li>
</ol>

<li>Generate the fake data: <b>python manage.py shell < tasks/fakedata.py</b> </li>
<li>Optionally create a custom Django admin for access to the admin interface: <b>python manage.py createsuperuser</b> </li>

<li>Run the project: <b>python manage.py runserver</b> </li>
</ol>
