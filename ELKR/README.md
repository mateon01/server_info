Elasticsearch Service + Logstash(Beat) + Kibana + Redis
---
1. Elasticsearch 대용량 데이터 처리에 적합 하지 않음(실시간 인덱식 처리로 인한 메모리 과부하, JVM Mataspace로 힙 메모리 영역 제한이 없으나 G1GC 알고리즘에 부하를줌)
2. 내부적으로 분산 처리 되기 때문에 type을 pix로 하는 순간 검색에 문제가 생김.
3. Logstash의 기본 힙메모리 설정이 높아 Server 사양에 따라 유동적인 변경이 필요함.


Kafka VS Hadoop
---
1. Kafka : 실시간 분석 처리에 적합.
2. Hadoop : 대용량 데이터 분석 처리에 적합.
3. Redis : Kafka 대용으로 많이 사용 한다. 같은 힙 서버 개념으로 사용되며 분산 클러스터 노드 또한 지원하고 굉장히 가볍고 빠른 강력한 MDB 이다.

Elasticsearch
---
* indexer - data - searcher 로 구성되어 있음
* Elasticsearch data architecture 조회 플러그인 별도 서버에 설치 가능.
