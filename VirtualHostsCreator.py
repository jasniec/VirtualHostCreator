#!/usr/bin/python3

import sys
import os

domain_name = sys.argv[1]
etc_path = "/etc/apache2/sites-available/" + domain_name + ".conf"
www_path = "/var/www/" + domain_name + "/public_html"

if os.system("mkdir " + www_path + " -p") == 0:
    raise Exception("mkdir: [FAIL]")
print("mkdir: [OK]")

if os.system(f'chmod -R 755 {www_path} > /dev/null') == 0:
    raise Exception("chmod: [FAIL]")
print("chmod: [OK]")

APACHE_LOG_DIR = "{APACHE_LOG_DIR}"
vhost = f'<VirtualHost *:443>\n    ServerName {domain_name}\n    ServerAlias www.{domain_name}\n    DocumentRoot /var/www/{domain_name}/public_html\n    ErrorLog ${APACHE_LOG_DIR}/{domain_name}-error.log\n    CustomLog ${APACHE_LOG_DIR}/{domain_name}-access.log combined\n    RewriteEngine on\n</VirtualHost>'

etc_f = open(etc_path, "a")
etc_f.truncate(0)
etc_f.write(vhost)
etc_f.close()

print("file: [OK]")

if os.system("a2ensite " + domain_name) == 0:
    raise Exception("a2ensite: [FAIL]")
print("a2ensite: [OK]")

if os.system("systemctl restart apache2") == 0:
    raise Exception("apache restart: [FAIL]")
print("apache2 restart: [OK]")

if os.system(f'certbot certonly --redirect --noninteractive --agree-tos --cert-name {domain_name} -d {domain_name} --register-unsafely-without-email --webroot -w {www_path}') == 0:
    raise Exception("certbot: [FAIL]")
print("certbot: [OK]")
