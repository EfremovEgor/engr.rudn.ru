# Развертывание сайта

- [Требования](#требования)
- [Установка SSH-сервера](#установка-ssh-сервера)
- [Настройка SSH-сервера](#настройка-ssh-сервера)
- [Установка SSH на Windows 10/11](#установка-ssh-на-windows-10/11)

## Требования

- Удаленный сервер под Ubuntu 22.04 LTS

## Установка SSH-сервера

Обновить репозиторий:

```
$ sudo apt update
```

Установить SSH:

```
$ sudo apt-get install ssh
```

Установить SSH-сервер:

```
$ sudo apt install openssh-server
```

Добавить SSH-сервер в автозагрузку:

```
$ sudo systemctl enable sshd
```

Проверить работу SSH:

```
$ systemctl status sshd
```

Результат выполнения команды должен быть таким:

![alt text](./images/sshd_status.png)

## Настройка SSH-сервера

Открыть файл конфигурации SSH-сервера:

```
$ sudo nano /etc/ssh/sshd_config
```

![alt text](./images/sshd_config_default.png)

Раскомментировать строчку:

```
#Port 22
```

Желательно изменить порт на любой другой:

![alt text](./images/ssh_config_edited.png)

Перезапустить SSH-сервер:

```
systemctl restart sshd
```

## Установка SSH на Windows 10/11

Открыть Windows PowerShell от имени администратора

Установить SSH-клиент:

```
Add-WindowsCapability -Online -Name OpenSSH Client~~~~0.0.1.0
```

Проверить установку:

```
Get-WindowsCapability -Online | ? Name -like 'OpenSSH*'
```

![alt text](./images/windows_ssh_installed.png)
