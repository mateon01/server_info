대용량 데이터 처리(MySql 튜닝)
---

* 현상황
  - Database(MySql)
    - Single Instance
    - DB Instance class : db.m4.large
    - Storage : 100GB
    - Storage Type : General Purpose(SSD)
    - core : 2core
    - Memory : 8Gb
  - Application(WAS)
    - ELB/Multi Instance(AutoScaling Enable)
    - t2.small * n (Autoscaling 에 따라 증설)
    - CPU : 1core
    - Memory : 2Gb
    - JDK Version : 1.7
    - WAS : Tomcat7
    - Container : ri, 4D_Cloud
    - Third party : Logstash, Zabbix agent
  - ElasticSearch
    - t2.medium * 3(Clustering)
    - Storage : 35Gb * 3

* 요구 사항
  - 분당 20,000건 데이터 처리 필요(333/TPS)
  - 월당 864,000,000건 라이선스 발급 이력 저장(250GB/Monthly)

* 개선 방안
  - 인프라 구성
  ![Alt text](https://github.com/mateon01/server_info/blob/master/img/infra.png?raw=true)
  - Application server
    1. ELB, AutoScaling를 통한 분산 처리.
      - Latency에 따른 Scale up/down
      - 기본 가용 Instance 증가(2 -> 6 or 10)
    2. JVM(WAS) 튜닝
      ![Alt text](https://github.com/mateon01/server_info/blob/master/img/jvm.jpg?raw=true)
      - -Xss<Sizs> //Stack사이즈(스텍 사이즈의 레퍼런스 확인이 어려움)
      - -Xms2048m
      - -Xmx2048m
      - -XX:MinHeapFreeRatio=2048m
      - -XX:MaxHeapFreeRatio=2048m
      - -XX:TargetSurvivorRatio=70 //Survivor Area 가 Minor GC를 유발하는 비율(Default=50)
      - -XX:+DisableExplicitGC //System.gc() 함수 방지
    3. Logstash, Tomcat의 메모리 사용율을 고려한 인스턴스 타입 변경
      - t2.medium * n (Autoscaling 에 따라 증설)
      - CPU : 2core
      - Memory : 4Gb
  - 데이터 베이스 처리 개선.
    1. Mysql Sharding(Read replication - 2중 커넥션 및 Proxy 레퍼런스 부족)
    2. 테이블 파티셔닝 및 클러스터 인덱스, 리버스 인덱스 적용
    3. 내부 망으로 변경, Haproxy 솔루션을 이용하여 접근 제어.
  - 라이선스 발급 이력 개선.
    1. 데이터 웨어하우스 사용(ex. RedShift).
    2. S3 저장 후 일일 배치로 데이터 웨어하우스에 copy.
    3. Zeppelin을 이용한 데이터 분석 기능 추가.
    4. 로그 발생량에 따른 ElasticSearch 클러스터 추가.
    5. 실시간 조회의 견우 ElasticSearch API를 사용, 이전 발급 이력에 대한 조회 분석은 Redshift를 사용.
    6. 내부망으로 변경, Haproxy 솔루션을 이용하여 접근 제어.

* 이슈 사항
  - Redshift의 응답 속도(일반적인 데이터 베이스보다 느림)
    - 직접 적인 커넥션이 아닌 로그 조회용의 경우 큰게 문제 없음
  - S3 비용 이슈
    - 일일 배치로 해결.
  - 발급 이력 조회 기간이 제한
    - ES 용량의 한계, 실시간 이력 조회의 경우는 매우 제한적.
    - 하루 전 데이터까지 조회는 Redshift를 사용하기 때문에 응답은 느리나 가능함.
  - CPAdmin 전체 로직 고도화 진행 필요
