# jupyter-openbis-integration-service

This is a small webservice which allows openbis to create a jupyter notebook inside the user-space of a Jupyterhub installation. It returns the location of the created jupyter notebook file and thus allows to establish a direct link from ELN-LIMS into this jupyter notebook.

### Requirements

The webservice requires the well-established tornado webserver. There are no other known dependencies.

### Installation is easy:

```
pip install jupyter-openbis-integration-service
```

### Running the server:

```
jupyter_openbis_integration_service --openbis https://openbis.domain:port 
```

**Optional settings**

The server is listening on port 8123 per default. You can change this with the --port switch:

```
--port 8123 
```

with the `--create-users` switch set, users are automatically created on the system. This is still experimental.

```
--create-users
```

With the `--cert' and `--key' switch set, the service will start using https instead http

```
--cert
--key
```

### Running the server behind nginx / Apache

This webservice does not support https and should always be routed by a proxy server, such as nginx or Apache. This means, the proxy server handles the https and sends all incoming requests on endpoint `/jupyter-openbis-integration-service` internally to port 8123 on the same machine. For **nginx**, the configuration may look like this:

```
location /jupyter-openbis-integration-service {
    proxy_pass http://129.132.80.90:8123;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_read_timeout 20d;
}
```
For production, do not use `localhost`, because on a machine with several IP addresses this will bind the proxy-server to all available addresses on port 8123. 


For **Apache**, the configuration looks quite similar:

```
LoadModule proxy_module modules/mod_proxy.so
<Location /jupyter-openbis-integration-service>
    ProxyPass http://129.132.80.90:8123
    ProxyPassReverse http://129.132.80.90:8123
</Location>
```

### Functionality

Request

```
https://some.jupyterhub.server/jupyter-openbis-integration-service?token=username-ADHXCHFAKHFP9ZAIUWRT34792KWEFKDSHB238FA9&folder=test&filename=testFile.txt&test=True
```
(if you add the test=True flag, the file will not be written)

The webservice will respond like this:

```
{
    "fileName": "testFile.txt",
    "path": "/home/username/test/testfelchen.txt"
}
```

If anything fails, an https status code ≠ `2xx` will be returned. The body will contain the error message like so:

```
HTTP-Status: 401 unauthorized
{
    "message": "token is invalid",
    "token": "username-ADHXCHFAKHFP9ZAIUWRT34792KWEFKDSHB238FA9"
}
```