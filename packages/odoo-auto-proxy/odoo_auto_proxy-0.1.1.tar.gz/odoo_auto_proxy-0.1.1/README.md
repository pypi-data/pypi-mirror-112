# Odoo Nginx Proxy



### Install

Using pip3 on local system:

```bash
pip3 install odoo_auto_proxy
```



In docker environment

```bash
docker run -d -v "$PWD/../nginx_conf:/etc/nginx/conf.d" -e NGINX_CONTAINER_NAME=odoo -e URL_DOMAIN=localhost odoo_auto_proxy
```



### Run

```bash
mkdir nginx_conf
docker run -d -v "$PWD/../nginx_conf:/etc/nginx/conf.d"  -p 80:80 --name odoo nginx

python3 -m odoo_reverse_proxy -c odoo -f ../nginx_conf
docker-compose -f exemple_odoo_compose.yml up
```



```bash
# Install certbot on nginx container
mkdir -p /var/www/letsencrypt
apt update
apt install -y software-properties-common
add-apt-repository ppa:certbot/certbot
apt update
apt install -y python-certbot-apache apt install gnupg
apt install -y certbot
apt install -y python-certbot-nginx
```



If this is not working, the generated template may be wrong. Check it by running:

```bash
docker exec odoo nginx -s reload
```

where `odoo` is your nginx container





### Issues

* Port is lost with redirection: accessing `odoo_server.localhost:8000` redirect us to `odoo_server.localhost/web`, we can only use port 80 (and maybe 443) as forward for nginx
* Some values are override manually (web_upstream, proxy_pass and poll_upstream): remove them from config and template?



### TODO

* Add certbot support
* Make the python program available on pypi
* Create dockerfile, docker image and docker-compose for the service