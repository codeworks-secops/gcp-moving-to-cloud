# Motivations

- Learn and practice a new stuff like `Python` and `Flask`
- Deploy a Python app in the `GCP` Cloud Provider using `GKE - Google Kubernetes Engine`

# What about our Application ?

The goals of our sample greeting application are multiple : 
 
- Say `Hello from CodeDay!` when the `/hello` route is invoked
- Say `I'm hamza from CodeDay!` when the `/hello/hamza` route is invoked
- Display an increment counter each time we visit one of the previous routes


# Installation & Build Steps


1- Install Python
===

```bash
# Check the Python installation
python --version
```
2- Install Pip
===

```bash
# Update your system dependencies
sudo apt update
# Intall pip
sudo apt install python3-pip
# Check the Pip installation
pip3 -V
pip3 --version
```

3- Install Flask
===

```bash
# Install flask using pip
pip3 install flask
# Check the Flask installation
flask --version
```

4- Run the app
===

```bash
# Export FLASK_APP environment variable to tell the terminal, the application to work with
export FLASK_APP=app.py
# Run the Flask application
flask run
# Check url access (on terminal or browser) 
localhost:5000
```

# Are you ready to go Cloud ?