

# **[push_notifications_server](https://github.com/marianhoenscheid/push_notifications_server)**

Um die Firebase Integration zu ermöglichen wird serviceAccountKey.json benötigt. Diese kann in der Firebase Konsole heruntergeladen werden. Anschließend muss der Pfand zur Datei der Variable _auth_file_ zugeordnet werden.

Um eine sichere Verbindung zu ermöglichen wird ein SSL Zertifikat und ein Private Key benötigt. Die Pfade zu den Dateien müssen in _key_file_ und _cert_file_ gespeichert werden.

Der Port kann durch die Variable _port_ konfiguriert werden

**HTTPS API:**

**POST /register**

```json 
{
	"client_name":"<name>"
	"token":"<token>"
}
```

```shell
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"client_name":"<name>","token":"<token>"}' \
  https://<ip>:8000/register
```

Antwort des Servers

```json
saved
```

**GET /clients**

```shell
curl https://<ip>:8000/clients
```

Antwort des Servers

```json
{"<name>": {"token": "<token>"}}
```

 **POST /send**

```json
{
    	"token":"<token>"
    	"title":"<titel>"
    	"body":"<text>"
    	"img_url":"<url>"     	 //optional
}
```

```shell
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"token":"<token>","title":"<titel>","body":"<body>"}' \
  https://<ip>:8000/send
```

Antwort des Servers

```json
{"id": "<message_id>"}
```