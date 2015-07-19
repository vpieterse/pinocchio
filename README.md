-------------
# Pinocchio
-------------

### Getting started
- Install Django (https://www.djangoproject.com/start/)
- For help with Git visit: http://rogerdudler.github.io/git-guide/
- Fork and clone this repository. Or you could just clone it directly but it's generally better to fork it first. (If you're not added as a contributor then you ***have*** to fork it first)
- To start the server use: `python manage.py runserver`
- For a sample page visit http://127.0.0.1:8000/peer/fileUpload.

### Models
- Check out `pinocchio/peer_review/models.py`

### Sample page
This is the file manager page for Pinocchio with working file upload.

- Go to `pinocchio/peer_review/templates/peer_review/fileUpload.html` for the template
- Resources (CSS, JavaScript) are under `pinocchio/peer_review/static/peer_review/`
- Uploaded files go to `pinocchio/media`

Question admin page is showing but functionality not added yet
- `http://127.0.0.1:8000/peer/questionAdmin`

### Admin page
- Go to http://127.0.0.1:8000/admin/.
Log in with:
  - Username: `admin`
  - Password: `admin`

-------------
