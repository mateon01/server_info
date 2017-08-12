Using open Host-Base IPS/IDS with AWS
=====
![Alt text](https://github.com/mateon01/server_info/blob/master/img/networks.png?raw=true)
__Architecture__

Introduce
---

Suricata is a fast and powerful network threat detection engine matured with open source IPS / IDS. The engine uses pattern matching and is designed for multi-threaded, high-volume data processing.

We introduced a host-based method to use for large-capacity cloud service, and log of Suricata and Application Server was visualized using Logstash and AWS ES.

The above architecture has a private zone configuration and Nat Instance is used to manage each server.

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

* Running Suricata
<pre><code>#Check if suricata supports birdge IPS mode
suricata --build-info |grep NFQueue
  NFQueue support:                         yes

#Bridge Running in IPS mode
sudo suricata -c /etc/suricata/suricata.yaml -q 0

#Send traffic coming into birdge to IPS
sudo iptables -A FORWARD -j NFQUEUE
</code></pre>

Nginx Setting
---
* Give the resolver option because ELB is the target
<pre><code>server {
      keepalive_timeout 10;
      listen       80;
      location / {
                resolver 172.32.0.2 valid=10s;
                set $backend "http://[ELB URL]";
                proxy_pass $backend;
                charset utf-8;
        }</code></pre>

Tip
---
* Each server instance type should be stress tested thoroughly.
* Signature rules of suricata should be created and applied customized if you have specified specifications.
* In IDS mode, please collect enough log for more than one month, analyze it and apply signature.


Issue
---
* When blocking normal packets
  * Do not use the default signature rules. In IDS mode, collect logs for more than one month, analyze them, and create signature rules for each one.
  * If a normal packet is blocked by a custom signature rule, you have to manually release it.
* nf_queue: fail at **** entries, dropping packets (s)
  * The error is that the suricata queue has a large number of packets and the network is disconnected due to DHCP call delay.
  * The fail-open feature will not scan packets if the queue is full. If this is the case, there may be a security problem.
  * Load test to find suitable memory and reset the server.

Result
---
Suricata is a powerful and good engine, but as with all open source, there are no detailed requirements. Test results show that suricata is overwhelming in CPU and memory usage, and in case of large capacity, nf_queue error is likely to occur as in Issue.

Of course, you can solve the problem with enough testing, but the human resources are quite significant, and even if you apply it, there is a problem with the control.


If there is a lack of control personnel or difficulty in testing, we recommend using commercial services.
