# Build images
```
eval $(minikube docker-env)
cd containers
docker build omero-web -t omero-web
docker build omero-server -t omero-server
cd ../k8s_ymls
# NFS setup? docker container (because kub not privileged)
kubectl apply -f omero-secrets.yml
kubectl apply -f postgres.yml
kubectl apply -f omero-server.yml # failing currently on nfs mount
kubectl apply -f nginx_conf_http.yml
kubectl apply -f nginx.sslsecret.yml
kubectl apply -f omero-rw-web.yml
kubectl port-forward svc/omero-web 6080:4080 --address==0.0.0.0
```


Should be:
```
omero-server@omero-readonly-server-bbb46b697-v6x4h:/OMERO/certs$ ls
server.key  server.p12  server.pem
```

```
Running /startup/55-certs.sh 
OpenSSL 1.1.1n  15 Mar 2022
Can't open /OMERO/certs/server.pem for writing, Read-only file system
140289759524032:error:0200101E:system library:fopen:Read-only file system:../crypto/bio/bss_file.c:69:fopen('/OMERO/certs/server.pem','w')
140289759524032:error:2006D002:BIO routines:BIO_new_file:system lib:../crypto/bio/bss_file.c:78:
pkcs12: Can't open "/OMERO/certs/server.p12" for writing, Read-only file system
certificates created: /OMERO/certs/server.pem /OMERO/certs/server.p12
```

Currently is:
```
omero-server@omero-server:/OMERO/certs$ ls
ffdhe2048.pem  server.key  server.p12  server.pem
```

```
Running /startup/55-certs.sh 
OpenSSL 1.1.1n  15 Mar 2022
Traceback (most recent call last):
  File "/opt/omero/server/server_venv/bin/omero", line 8, in <module>
    sys.exit(main())
  File "/opt/omero/server/server_venv/lib/python3.7/site-packages/omero/main.py", line 126, in main
    rv = omero.cli.argv()
  File "/opt/omero/server/server_venv/lib/python3.7/site-packages/omero/cli.py", line 1787, in argv
    cli.invoke(args[1:])
  File "/opt/omero/server/server_venv/lib/python3.7/site-packages/omero/cli.py", line 1225, in invoke
    stop = self.onecmd(line, previous_args)
  File "/opt/omero/server/server_venv/lib/python3.7/site-packages/omero/cli.py", line 1302, in onecmd
    self.execute(line, previous_args)
  File "/opt/omero/server/server_venv/lib/python3.7/site-packages/omero/cli.py", line 1384, in execute
    args.func(args)
  File "/opt/omero/server/server_venv/lib/python3.7/site-packages/omero_certificates/cli.py", line 33, in certificates
    m = create_certificates(omerodir)
  File "/opt/omero/server/server_venv/lib/python3.7/site-packages/omero_certificates/certificates.py", line 135, in create_certificates
    with open(grouppath, "w") as pem:
OSError: [Errno 30] Read-only file system: '/OMERO/certs/ffdhe2048.pem'
```

omero-server
```
Generating RSA private key, 2048 bit long modulus (2 primes)
..+++++
............+++++
e is 65537 (0x010001)
certificates created: /OMERO/certs/server.key /OMERO/certs/server.pem /OMERO/certs/server.p12
```


Local:
```
Commands:   java -version                  11.0.18   (/usr/bin/java)
Commands:   python -V                      3.7.3     (unknown)
Commands:   icegridnode --version          not found
Commands:   icegridadmin --version         not found
Commands:   psql --version                 11.20     (/usr/bin/psql)
Commands:   openssl version                1.1.1     (/usr/bin/openssl)

Component:  OMERO.py                       5.16.0
Component:  OMERO.server                   5.6.8-ice36

No icegridadmin available: Cannot check server list

Log dir:    /opt/omero/server/OMERO.server/var/log exists
Log files:  Blitz-0.log                    950.7 KB      errors=0    warnings=2   
Log files:  DropBox.log                    n/a
Log files:  FileServer.log                 n/a
Log files:  Indexer-0.log                  6.1 KB        errors=0    warnings=2   
Log files:  MonitorServer.log              n/a
Log files:  PixelData-0.log                3.6 KB        errors=0    warnings=2   
Log files:  Processor-0.log                64.1 KB      
Log files:  Tables-0.log                   1.1 KB       
Log files:  TestDropBox.log                n/a
Log files:  master.err                     2.3 KB       
Log files:  master.out                     empty
Log files:  Total size                     1.03 MB


Environment:OMERO_HOME=(unset)             
Environment:OMERODIR=/opt/omero/server/OMERO.server 
Environment:OMERO_NODE=(unset)             
Environment:OMERO_MASTER=(unset)           
Environment:OMERO_USERDIR=(unset)          
Environment:OMERO_TMPDIR=(unset)           
Environment:PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin 
Environment:PYTHONPATH=(unset)             
Environment:ICE_HOME=(unset)               
Environment:LD_LIBRARY_PATH=(unset)        
Environment:DYLD_LIBRARY_PATH=(unset)  
```


gcp:
```
Commands:   java -version                  11.0.18   (/usr/bin/java)
Commands:   python -V                      3.7.3     (unknown)
Commands:   icegridnode --version          not found
Commands:   icegridadmin --version         not found
Commands:   psql --version                 11.20     (/usr/bin/psql)
Commands:   openssl version                1.1.1     (/usr/bin/openssl)

Component:  OMERO.py                       5.15.0
Component:  OMERO.server                   5.6.8-ice36

No icegridadmin available: Cannot check server list

Log dir:    /opt/omero/server/OMERO.server/var/log exists
Log files:  Blitz-0.log                    3.1 MB        errors=0    warnings=3   
Log files:  DropBox.log                    n/a
Log files:  FileServer.log                 n/a
Log files:  Indexer-0.log                  27.0 KB       errors=0    warnings=2   
Log files:  MonitorServer.log              n/a
Log files:  PixelData-0.log                13.2 KB       errors=0    warnings=2   
Log files:  Processor-0.log                977 B        
Log files:  Tables-0.log                   1.3 KB       
Log files:  TestDropBox.log                n/a
Log files:  master.err                     2.3 KB       
Log files:  master.out                     empty
Log files:  Total size                     3.11 MB


Environment:OMERO_HOME=(unset)             
Environment:OMERODIR=/opt/omero/server/OMERO.server 
Environment:OMERO_NODE=(unset)             
Environment:OMERO_MASTER=(unset)           
Environment:OMERO_USERDIR=(unset)          
Environment:OMERO_TMPDIR=(unset)           
Environment:PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin 
Environment:PYTHONPATH=(unset)             
Environment:ICE_HOME=(unset)               
Environment:LD_LIBRARY_PATH=(unset)        
Environment:DYLD_LIBRARY_PATH=(unset) 
```

gcp (no ff... file)
omero-certificates 0.2.0

local
omero-certificates 0.3.0