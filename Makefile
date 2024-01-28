update:
	 git pull https://github.com/EfremovEgor/engr.rudn.ru.git
	 python3 src/manage.py collectstatic --no-input 
	 python3 src/manage.py migrate 
	 sudo systemctl restart gunicorn

create_env:
	echo "DJANGO_DATABASE_HOST= \nDJANGO_DATABASE_PORT= \nDJANGO_DATABASE_NAME= \nDJANGO_DATABASE_USER= \nDJANGO_DATABASE_PASSWORD= " >> .env

run_tests:
	cd src && coverage run manage.py test 