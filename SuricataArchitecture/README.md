Using open Host-Base IPS/IDS with AWS
=====
![Alt text](https://github.com/mateon01/server_info/blob/master/img/networks.png?raw=true)
__Architecture__


# Install Suricata
---

Features
---
* Suricata : IPS/IDS
* Nginx : Reverse proxy
* Redis : Redis is used as an intermediate data collection queue in case the log accumulates quickly
* Logstash : Logstash for collecting logs is activated on each server.

Requirements
---
* Suticata Ver3.2.3
* Nginx Ver1.12.1
* Logstash Ver2.0.0

Install Suricata
---

<pre><code>yum install epel-release

#Installing dependency packages
sudo yum -y install gcc libpcap-devel pcre-devel libyaml-devel file-devel \
  zlib-devel jansson-devel nss-devel libcap-ng-devel libnet-devel tar make \
  libnetfilter_queue-devel lua-devel

#Download Suricata
wget http://www.openinfosecfoundation.org/download/suricata-3.2.3.tar.gz

#Suricata Uncompress and move to that directory
#IPS uses NFQ, an option must be given.
./configure --prefix=/usr/ --sysconfdir=/etc/ --localstatedir=/var/ --with-libjansson-libraries=/usr/lib64 --with-libjansson-includes=/usr/include --enable-lua --enable-nfqueue

#Install Suricata
#You can view Build information with Build-info Command
make && make install && ldconfig
make install-full
suricata --build-info
</code></pre>

* Libjansson.so.4 when an error occurs

<pre><code>wget http://www.digip.org/jansson/releases/jansson-2.9.tar.gz

./configure
make
make check
make install

cd /usr/local/lib
ln -s /usr/local/lib/libjansson.so.4 /usr/lib/libjansson.so.4
</code></pre>
