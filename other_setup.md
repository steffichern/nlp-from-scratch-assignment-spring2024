## Follow this link to install postgresql database

https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql-linux/


## Create a user named "711-rag" with a password(whatever you want)

connect to psql as default user

```
sudo -u postgres psql
```

create user 

```
CREATE USER "711-rag";
```

set password 

```
ALTER USER "711-rag" PASSWORD '<password>';
```

allow this user to create databse
```
ALTER USER "711-rag" CREATEDB;
```

exit
```
\q
```


Then set environment variable for the password
```
export PG_PASSWORD_RAG="<password>"
```

When you run the code, make sure postgres is running
```
sudo systemctl start postgresql
```

## Install pgvector extension

See: https://github.com/pgvector/pgvector?tab=readme-ov-file#linux-and-mac

```
cd /tmp
git clone --branch v0.6.1 https://github.com/pgvector/pgvector.git
cd pgvector
make
make install # may need sudo
```

## Set up ollama, the tool for running local LLMs.

See https://github.com/ollama/ollama

But basically we should only need to do two things

1. Install ollama:

```
curl -fsSL https://ollama.com/install.sh | sh
```

2. make sure it's running when you run the code

```
ollama serve
```

So for background stuff, we need make sure both ollama and postgres running when we run the code.

## Authenticaction issue

I found that I couldn't connect to psql with correct password after I set up the user. I tried to login with command 

```
psql -U 711-rag -W
```

then typed correct password but I got
 

`psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  Peer authentication failed for user "711-rag"`


I found this chatgpt-generated solution useful:

To solve this issue, you need to edit the pg_hba.conf file to change the authentication method from "peer" to "md5" for the connection you are trying to make (which uses a password to authenticate). Here's how you can do it:

Locate the pg_hba.conf file. This file is usually found in the PostgreSQL data directory, which varies based on how PostgreSQL was installed. Common locations include `/etc/postgresql/<version>/main` or `/var/lib/postgresql/<version>/main`, where <version> is your PostgreSQL version(our is 16). You can often find the exact path by running sudo -u postgres psql -c "SHOW hba_file;" in your terminal.

Open the pg_hba.conf file in a text editor (you'll need superuser privileges to edit it). Look for lines that look like this:

```
TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     peer
```
Change the METHOD from peer to md5 for the line that's relevant to your connection. If you want to apply this change universally, you could change it for the "all" DATABASE and USER fields, but be cautious as this affects all local connections:

```
TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     md5
```
Save the file and exit the editor.

Restart the PostgreSQL service for the changes to take effect. You can typically do this with a command like `sudo systemctl restart postgresql`, though the exact command might vary depending on your system setup.