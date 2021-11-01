# How to Start H2 Database

## Prerequisite
- [Java](https://java.com/en/download/help/download_options.html)
- [h2.jar](https://mvnrepository.com/artifact/com.h2database/h2)
- the commands below are ran in the `python-spark-training/data-streaming-service` path 

## Step 1 - Create a new database

You can create a local database from the command line\
`java -cp h2/h2.jar org.h2.tools.Shell`
```
Welcome to H2 Shell
Exit with Ctrl+C
[Enter]   jdbc:h2:mem:2
URL       jdbc:h2:./h2/test-db;MODE=PostgreSQL;DATABASE_TO_UPPER=false;INIT=RUNSCRIPT FROM './h2/h2-dbschema.sql';
[Enter]   org.h2.Driver
Driver
[Enter]   sa
User      test
Password  (hidden)
Type the same password again to confirm database creation.
Password  (hidden)
Connected

sql> quit
```
*you might need to change*  `URL INIT=RUNSCRIPT FROM './dbschema.sql';` *depending on your path*

**At this point your database is ready to be used**

## Step 2 - launch server
You can launch user interface server by running\
`java -Dh2.bindAddress=127.0.0.1 -cp h2/h2.jar org.h2.tools.Server -baseDir ./h2`

## Step 3 (optional) - login to server
Running step 2 should open the login window in your default browser but you can also get there by going to `http://localhost:8082/login.jsp`

```
JDBC URL: jdbc:h2:./test-db
User Name: test
Password: (hidden)
```

### voila