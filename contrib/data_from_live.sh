#!/bin/sh


mysqldump -u planlos -p planlosdev_db > planlos_dev.sql
mysql -u planlos -p --database planlostest < planlos_dev.sql

cp -ar /srv/www/planlosbremen.de/www/media/images/flyer/* /srv/www/planlosbremen.de/images/flyer/
cp -ar /srv/www/planlosbremen.de/www/media/images/location/* /srv/www/planlosbremen.de/images/location/
