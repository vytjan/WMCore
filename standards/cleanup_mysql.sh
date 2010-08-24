#!/bin/sh

echo "-->remove database from database server"
if test -r $DBSOCK 
then
    echo 'using socket'
    echo "-->remove database from database server"
    mysql -u $DBMASTERUSER --socket=$DBSOCK --exec "drop database ${DBNAME}"
    echo '-->Using mysql DB: ' $DATABASE
    mysql -u $DBMASTERUSER --socket=$DBSOCK --exec "${SQLCREATE}"
    mysql -u $DBMASTERUSER --socket=$DBSOCK --exec "create database ${DBNAME}"

    mysql -u $DBMASTERUSER --socket=$DBSOCK --exec "drop database ${PROXYDB}"
    echo '-->Using mysql DB: ' $PROXYDATABASE
    mysql -u $DBMASTERUSER --socket=$DBSOCK --exec "${PROXYCREATE}"
    mysql -u $DBMASTERUSER --socket=$DBSOCK --exec "create database ${PROXYDB}"
else
    echo 'using host: ' $DBHOST
    mysql -u $DBMASTERUSER --password=$DBMASTERPASS -h $DBHOST --exec "drop database ${DBNAME}"
    echo '-->Using mysql DB: ' $DATABASE
    mysql -u $DBMASTERUSER --password=$DBMASTERPASS -h $DBHOST --exec "${SQLCREATE}"
    mysql -u $DBMASTERUSER --password= $DBMASTERPASS -h $DBHOST --exec "create database ${DBNAME}"

    mysql -u $DBMASTERUSER --password=$DBMASTERPASS -h $DBHOST --exec "drop database ${PROXYDB}"
    echo '-->Using mysql DB: ' $PROXYDATABASE
    mysql -u $DBMASTERUSER --password=$DBMASTERPASS -h $DBHOST --exec "${PROXYCREATE}"
    mysql -u $DBMASTERUSER --password=$DBMASTERPASS -h $DBHOST --exec "create database ${PROXYDB}"
fi


