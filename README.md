### Prerequisites

You need to have Python on your system.

If you are going to use virtualenv to create standalone environment, make sure you have it set up
```
pip install virtualenv
```


## How to Run the App

1. Open cmd and make a directory where you'd be cloning the repo.
```
  mkdir unposed_dir
```
* if you are not going to use virtualenv, you can directly clone the repo without having to make a directory.

2. Next, go to the directory you just created and set up a virtual environemnt. If you are not using virtualenv, you can skip to step 4.
```
cd unposed_dir
virtualenv unposed_env
```
* This will create a another directory where all the dependencies will be set.

3. Next, activate the virtual environment.
```
source unposed_env/bin/activate
```

4. Now, clone the repo by running
```
git clone https://github.com/Zlash65/UnPosed.git
```

5. Next step is to set up all the requirements to run the project
```
cd UnPosed
pip install -r requirements.txt
```

6. Once all the requirements are set up, you need to set up models that will be used.
```
python manage.py makemigrations
python manage.py migrate
```

7. Everything is set up and you can run the project using the following command
```
python manage.py runserver
```
* When you run it for the first time, it will pull data from flickr and create dummy users.
* It should take about a couple minutes before the actual start.
* If you see something like `Starting development server at http://127.0.0.1:8000/`, run it in browser.
* To deactivate the virtualenv, simply run `deactivate` in terminal
