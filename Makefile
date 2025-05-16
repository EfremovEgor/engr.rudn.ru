update:
	 git pull https://github.com/EfremovEgor/engr.rudn.ru.git
	 python3 src/manage.py collectstatic --no-input 
	 python3 src/manage.py migrate 
	 python3 src/manage.py compilemessages
	 sudo systemctl restart gunicorn
	 docker compose restart

create_env:
	echo "DJANGO_DATABASE_HOST= \nDJANGO_DATABASE_PORT= \nDJANGO_DATABASE_NAME= \nDJANGO_DATABASE_USER= \nDJANGO_DATABASE_PASSWORD= \nPROMETHEUS_URL_SUFFIX= \nDJANGO_DATABASE_PASSWORD= \nDJANGO_ADMIN_URL_SUFFIX=" >> .env

run_tests:
	cd src && coverage run manage.py test 

push:
	git add *
	git commit -m "push"
	git push origin main
