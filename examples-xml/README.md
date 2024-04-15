# XML examples

This directory contains the examples described in the assignment if
you need to debug the requests something with more details. You need
to change the xml parameters by hand and send the request to the
server.

To send the requests you can use some tools like Postman or even
curl. With curl it is possible to send a xml request with the
following command:

```
curl -X POST -H "Content-Type: text/xml" -H "Cache-Control: no-cache" --insecure http://127.0.0.1:8888/ --data @clear-playlist.xml
```

Where you can change the `127.0.0.1` and `8888` with the ip and port
where the DeeJay server is running.

Obs: if you use the curl command, don't forget the `@` before the
file, otherwise the curl wont read the path as a file to be sent.
