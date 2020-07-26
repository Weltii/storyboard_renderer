install:
	pip3 install -r requirements.txt

test:
	 coverage run -m unittest discover backend/

start:
	uvicorn main:app --reload # Todo runs with the old main

increase_file_watches:
	sudo sysctl fs.inotify.max_user_watches=500000