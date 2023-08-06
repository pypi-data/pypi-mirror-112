# Vulseek Command Line Interface

## Installation / Upgrade

```
apt-get install -y python3 python3-pip python3-requests python3-click

pip3 install --user --upgrade vulseek
```

## Login

```
vulseek login https://qa.vulseek.io
username: fportantier@securetia.com
password: *************
```

## Session

```
vulseek session
{
    "username": "fportantier@securetia.com",
    "endpoint": "https://qa.api.vulseek.io"
}
```

## Logout

```
vulseek logout
```

## Upload File

```
vulseek upload /tmp/8.8.8.8.xml 
/tmp/8.8.8.8.xml: OK
```

