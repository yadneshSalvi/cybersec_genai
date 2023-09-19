Instructions to run the repo:

1. First install python 3.10.xx version, for your specific os if you do not have have python installed
   Link for windows 3.10.11 installer - https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe

2. If you do not have pip installed (run `pip` in terminal to check), install it using
   `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
   `python get-pip.py`

3. Create a virtual environment for this repo, either using your IDE (Visual Studio Code - ctrl+shift+p->Python:Create Environment), or through anaconda (need to install anaconda and run command `conda create --name myenv python=3.10`) or run following commands
    `pip install virtualenv`
    cd into the repo
    `python -m venv leah_sync`
    and to activate the env (should get activated automatically if done through IDE)
    `.\leah_sync\Scripts\activate`
    (and if created virtual env using conda run: `conda activate <name_of_env>`)

4. Finally install all requirements using
   `pip install -r requirements.txt`

5. To run the api use:
   `uvicorn main:app`