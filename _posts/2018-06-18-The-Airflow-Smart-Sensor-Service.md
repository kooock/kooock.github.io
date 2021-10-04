---
layout: post
title: The Airflow Smart Sensor Service 번역
excerpt: "Just about everything you'll need to style in the theme: headings, paragraphs, blockquotes, tables, code blocks, and more."
modified: 2021-10-04
tags: [airflow, smart sensor, airBnB, data engineering]
comments: true
---

# The Airflow Smart Sensor Service 번역


리소스 활용도 향상을 위한 장기 실행 경량 작업 통합

**By:** [Yingbo Wang](https://www.linkedin.com/in/yingbo-wang-86aa3027/), [Kevin Yang](https://www.linkedin.com/in/ruiqinyang/)

이 글은 [Yingbo Wang](https://www.linkedin.com/in/yingbo-wang-86aa3027/), [Kevin Yang](https://www.linkedin.com/in/ruiqinyang/)가 [에어비엔비 기술블로그에 작성한 글](https://medium.com/airbnb-engineering/the-airflow-smart-sensor-service-221f96227bcb)을 임의로 번역한 것입니다.

![https://miro.medium.com/max/1400/0*3r30u7rnBhR7BJSc](https://miro.medium.com/max/1400/0*3r30u7rnBhR7BJSc)

# Introduction

Airflow는 프로그래밍 방식으로 작성, 스케줄링, 모니터링 하는 데이터 파이프라인 플랫폼입니다. 기본적으로 Airflow 클러스터는 수천 개의 DAG(directed acyclic graphs: 방향이 있는 순환하지 않는 그래프)워크플로우를 지원합니다. 그리고 최고 수만 개의 task가 동시에 실행될 수 있습니다. 2018년으로 돌아가 보면, AirBnB의 Airflow 클러스터는 몇 천 개의 DAG를 가지고 있었고, 그보다 많은 3만개의 task가 동시에 돌고 있었습니다. 이러한 부하는 자주 AirBnB의 데이터베이스에 과중한 부하가 발생되도록 만들었습니다. 또한 이러한 동시에 실행되는 task를 지원하기 위해 수많은 리소스가 필요하기 때문에 클러스터의 비용이 상당히 커졌습니다.

시스템을 더 안정적으로 만들기 위해 그리고 클러스터의 비용을 줄이기 위해 우리는 Airflow 시스템을 최적화하는 방법을 찾았습니다. 우리는 장기실행경량(LRLW: Long-Running LightWeight) task가 많은 리소스를 낭비하고 있다는 사실을 파악했습니다. 그리고 우리는 이러한 LRLW task들을 통합하고 리소스 낭비를 해결하기 위한 Smart Sensor를 제안했습니다.

# Long-Running Lightweight Tasks

우리가 Airflow의 퍼포먼스 이슈들을 조사했을때, 우리는 일부 task 유형에서 LRLW와 같은 패턴을 보인다는 사실을 발견했다. 이러한 task들은 sensor task, subDAG 그리고 SparkSubmitOperator 등이 있다.

**sensor** 

sensor 또는 sensor task는 특정 기준을 충족할 때까지 실행되는 특수한 operator 유형이다. 이 기준은 HDFS 또는 S3에 랜딩하는 파일이거나, 하이브에 나타나는 파티션이거나, 다른 외부 task의 성공여부, 또는 하루 중 특정시간인 경우일 수 있다.

![https://miro.medium.com/max/700/0*HPMY9cRlDg7_Y7zj](https://miro.medium.com/max/700/0*HPMY9cRlDg7_Y7zj)

**Figure 1. The lifespan of a sensor task**

sensor task가 실행할 때, poke라고 부르는 함수가 보통 3분마다 주기적으로 기준 충족 여부를 체크합니다. 그리고 poke 함수가 true를 반환하면 ‘success’으로 기록하고 타임아웃일 경우 ‘fail’을 반환합니다. poke의 실행은 거의 100ms 이내로 상당히 빠릅니다. 그리고 대부분의 시간을 다음 poke가 실행될 때까지 기다리면서 idle 상태로 있습니다. sensor task의 수명은 체크타임부터 조건이 충족됐을 때까지 입니다. 이러한 수명은 몇분에서 몇일까지 될 수도 있습니다.

**SubDAGs**

**SubDAGs**는 LRLW task의 또 다른 예시입니다. 이 task는 DAG안의 일련의 task들을 캡슐화하고 복잡한 DAG구조를 깔끔하고 가독성있게 해줍니다. DAG run은 pre_execute 함수에서 subDAG에 대해 생성됩니다. 그 후 subDAG task는 execute function에서 DAG run의 상태를 "poke" 합니다.

**SparkSubmitOperator**

**SparkSubmitOperator** 또한 LRLW task입니다. Airflow의 Spark 클라이언트는 job을 제출하고 해당 job이 종료될 때까지 poll합니다. 이러한 모든 task는 어떤 작업이 초기화 된 이후 경량 상태로 빠지며, 때로는 장기실행 상태가 됩니다.

앞선 예시로부터 우리는 이러한 task들이 LRLW 패턴을 보인다는 사실을 확인할 수 있습니다. 이러한 task의 특징은 다음과 같습니다. 

- **리소스 활용성이 매우 낮음.** 이들 task에 대한 worker 프로세스 전체시간의 99%가량이 idle 상태로 남아있습니다.
- **이들 task는 대규모 클러스터에서 동시에 실행되는 task 중에서 매우 큰 비중을 차지하는 경우가 많음.** AirBnB에서는 실행되는 task의 70%이상이 sensor였습니다. 이 task들은 피크시간에 2만개 이상의 worker 슬롯을 차지했습니다.
- **많은 sensor task가 중복됨**. AirBnB의 sensor job의 40% 이상이 중복되어 있었습니다. 그 이유는 많은 downstream DAG가 일반적으로 중요한 몇 개의 upstream DAG를 동일한 파티션에서 기다리기 때문입니다.

# Smart Sensor

우리는 LRLW task의 통합을 위해 Smart Sensor를 제안했습니다. 원래 장기실행 sensor task를 통합할 목적으로 만들었지만 나중에 LRLW task를 통합하도록 확장되었습니다. 그렇지만 이 서비스의 이름을 Smart Sensor로 유지하였습니다.

# How It Works

Smart Sensor 서비스의 핵심 아이디어는 각 task마다 개별 process를 사용하는 대신에 장기 실행되는 task들을 일괄적으로 실행시키는 중앙화된 프로세스를 사용하는 것입니다.

![https://miro.medium.com/max/700/0*H6QTUtYBpgbn2ijm](https://miro.medium.com/max/700/0*H6QTUtYBpgbn2ijm)

**Figure 2. Sensors before and after enabling smart sensor**

Smart Sensor 서비스를 사용하면 sensor task는 두가지 과정으로 실행됩니다.

1. 첫번째 과정으로 각 task는 DAG를 파싱하여, task object를 가져온 다음, pre_execute 함수를 실행하고 스스로를 Smart Sensor 서비스에 등록합니다. 등록과정에서 외부 리소스를 poll하는데 필요한 정보를 Airflow metaDB에 저장하여 유지합니다. 그리고 등록이 성공하면 task는 빠져나가고 worker 슬롯에서 해제됩니다.
2. 그 이후, 몇 개의 중앙화된 process(DAG에 내장되어 있는 Smart Sensor task)들이 등록된 task들의 최근 레코드의 업데이트 여부를 확인하기 위해서 database를 지속적으로 체크하고 조건 충족하는 task에 대해서는 일괄적으로 poke 함수를 실행합니다. 
일반적으로 하나의 Smart Sensor task는 수백 개의 sensor task를 손쉽게 다를 수 있습니다. Smart Sensor는 또한 중복된 sensor task를 단일 인스턴스로 통합해서 더 많은 리소스를 절약할 수 있습니다.

**Smart Sensor는 sensor task shards를 정의하여 중복되는 작업을 제거하고 작업 부하의 균형을 맞춥니다.**  동시에 실행되는 sensor task가 많을 수 있습니다. 그리고 이 job들을 짧은 주기로 실행하기 위해 여러 개의 Smart Sensor task가 있을 것입니다. Smart Sensor에 sensor task가 할당되는 방법은 이 시스템을 설계할 때 우리의 도전과제 중에 하나였습니다. 우리는 모든 Smart Sensor task의 부하를 균형 있게 할당하기 위해 노력했습니다. 동시에 여러개의 poke 함수가 동일 대상에 대해 실행되지 않도록 중복된 sensor task가 반드시 같은 Smart Sensor에 할당되어야만 했습니다. 

![https://miro.medium.com/max/700/0*fM_bvm_cykKVz7qd](https://miro.medium.com/max/700/0*fM_bvm_cykKVz7qd)

**Figure 3. Deduplicating tasks by shardcode**

Smart Semsor 서비스에서 poke_context는 sensor job의 시그니처입니다. 이것은 sensor task의 poke함수가 실행되기 위해 필요한 argument들의 딕셔너리입니다. 같은 operator class와 동일한 poke_context를  가진 두개의 sensor는 같은 poke함수를 실행하면서 중복된 task로 취급합니다. poke_context의 해쉬코드를 사용하여 샤딩을 수행하고 각 Smart Sensor task가 특정 해쉬코드 범위에 있는 task를 처리하도록 함으로써, 중복된 sensor는 동일한 smart sensor로 할당됩니다. 해쉬코드가 길기 때문에 우리는 해쉬의 모듈러 연산을 통해 database에서 인덱싱 할 수 있도록 최적화하였습니다. 우리는 이 키를 shardcode라고 부릅니다.

Smart Sensor 서비스의 샤딩 작업의 방법은 그림 3에서 볼 수 있습니다. sensor1과 sensor2는 동일한 poke_cotext를 가지고 그렇기 때문에 같은 hashcode와 shardcode를 가집니다. 런타임에서 이들은 동일한 Smart sensor(예: SmartSensor1)에 의해 감지됩니다. 모든 중복된 sensor들은 하나의 poking 루프에서 한번만 poke 함수가 실행됩니다.

중앙화된 Smart Sensor task는 범용적인 프레임워크입니다. 이것은 가지각색의 class들을 지원하도록 설계되었습니다. class가 poke 함수를 가지고 이 poke 함수의 argument가 직렬화가 가능하다면 Smart Sensor task는 그 class를 지원할 수 있습니다.

**로그는 통합되지 않는 프로세스와 유사하게 취급됩니다.** task 실행이 더 적은 process들에 통합되어지더라도 Smart Sensor 서비스는 동일하게 Airflow UI에서 로그를 읽고 다룬로드 할 수 있도록 지원합니다. 유저는 원래 sensor의 task URL에 접속하여 로그를 읽을 수 있습니다.

**Smart Sensor는 손쉽게 Airflow 클러스터에 적용이 가능합니다.**

Smart Sensor 서비스를 사용하거나 사용하지 않게 하는 것은 간단합니다. 우리는 을 airflow.cfg의 smart_sensor 세션에서 시스템 레벨 configuration만 바꾸면 됩니다. 이 변화는 개별 유저에게는 가려지며 DAG를 개별 유저가 수정할 필요가 없습니다.  또한 중앙화된 smart sensor task이 로테이션 해도 유저의 sensor task가 실패하지 않습니다.

# The Efficiency Improvement

Smart sensor의 첫 버전을 개발할 때는 AirBnB는 피크시간에 동시에 수행되는 task의 60%이상을 줄일 수 있었습니다.  또한 동작하는 sensor task의 80%를 줄였습니다. 센서에 대한 프로세스 슬롯은 2만에서 80개로 줄어들었습니다. 실행 중인 task가 상당히 줄었기 때문에 database load 또한 크게 줄어들었습니다.

![https://miro.medium.com/max/700/0*lkiBWjq8_ezvYC-e](https://miro.medium.com/max/700/0*lkiBWjq8_ezvYC-e)

**Figure 4. Number of running tasks after Smart Sensor deployed**

smart Sensor에서 중복제거 메커니즘은 Hive metastore으로의 요청을 40%가량 줄였고 따라서 절대적인 sensor traffic과 기본 데이터 웨어하우스의 부하 모두 줄였습니다.

# Conclusion

Smart Sensor는 작고 가벼운 task의 traffic을 크고 중앙화된 task에 통합하는 서비스입니다. 이것은 Airflow infrastructure 비용을 줄이고 클러스터 안정성을 개선으로 이어질 수 있습니다. 이것은 특히 상당한 양의 sensor task가 있는 거대한 클러스터에 해당됩니다. AirBnB의 거대한 Airflow 클러스터의 경우 Smart sensor는 의미있는 수준의 비용절감과 클러스터 전체에 대한 엄청난 안정성 개선을 할 수 있게 하였습니다.

smart sensor 서비스는 [Apache Airflow 2.0](https://airflow.apache.org/docs/apache-airflow/stable/concepts/smart-sensors.html) majority한 새로운 기능 중에 하나로  릴리즈 되었으며 이후 더 많은 airflow 유저를 위한 리소스의 활용도를 개선하는데 사용되었습니다. smart sensor 서비스는 task 수명을 여러 프로세스로 분할하는 아이디어를 도입하고 task 실행을 위한 비동기 모드의 잠금을 해제했기 때문에 오픈소스 커뮤니티는 비동기 솔루션에 대한 보다 일반적인 유즈케이스에 투자하기 시작했습니다. 그 중 [deferrable (“Async”) operator](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=177050929) 는 비동기 모드를 더 많은 task로 확장하는 것을 목표로 하는 operator입니다.
