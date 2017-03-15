# Cybrary-login-automater
**get_cybytes.py** - script that automatically logs in for daily updates of cybytes and credits used on the website. https://www.cybrary.it/.

## Instructions:
> Install Python 2.x or 3.x (not tested but should work.
> Install libssl-dev libcurl4-openssl-dev python-dev using your favorite package manager (packages for Debian/Ubuntu, look for the same on other distros)
> Install pip (if you have not installed it yet).
  To install pip, download:  https://bootstrap.pypa.io/get-pip.py ,
  then run the following command:
  ```  
  python get-pip.py
  ```
> Optionally install [*virtualenv*](http://docs.python-guide.org/en/latest/dev/virtualenvs/) (pip install virtualenv)

> Once pip has been installed, run the following command:
  ```
  pip install -r requirements.txt --user <your_user>
  ```
The --user option is not neccessary if you use virtualenv

> Add the username and password values wherever required in the file **get_cybytes.py**

> Change the variable **CYBPATH** to the path of the dowloaded files in the files **get_cybytes.py** and **reschedule_jobs**.

> Keep all the files from the repo in the same folder. 

> Keep the last line of the file **cybrary.log** from the repo as it is and then run: `./reschedule_jobs` to schedule the cybytes
update job and forget about loggin in everyday :).
