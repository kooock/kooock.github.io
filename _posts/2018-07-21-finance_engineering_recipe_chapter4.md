---
layout: post
title: "[금융공학레시피 정리]주식, 가격, 지수"
excerpt: "금융공학 레시피 chapter4."
modified: 2018-07-22
comments: true
category : FinanceEngineering
tags: [금융공학, 퀀트]
---


금융공학 레시피 chapter4. 주식, 가격, 지수
--------------------------------------------------------------------------------------------

#### 4.1 주식과 가격
주식의 적정가격은 얼마일까?  => 아직 정확히 답을 아는 사람은 없음

하지만, 많은 사람들의 노력으로 다양한 valuation model이 개발됨

##### 주식가격은 기업의 과거, 현재, 미래를 반영

![useful image]({{ site.url }}/assets/images/samsung_stock_2016_6to2017_10.png)

2017년 마자막 날 삼성전자의 주가는 254만 8000원

과연 이 가격은 적정 가격일까? 썬건 아닐까? 비싼건 아닐까? 2016년 1월보다 많이 오른 것인가?

이런 답을 찾기 위해 기본적 / 기술적 분석 등 다양한 분석을 한다.

Analyst : 기업 실사, 미래 전망, 경쟁사 분석, CEO인터뷰 등 다양한 분석을 하고, 주가 예측을 위한 valuation => 목표 주가 산정/ 분석보고서 발간

##### 싸면 매수, 비싸면 매도 ~~아니 누가 모르나?~~

싸다고 생각하면 매수 : long position => position이 + 상태

비싸다고 생각하면 매도 : short position => position이 - 상태

주가는 더 많은 사람이 배팅하는 방향으로 움직임

##### 거래 발생 = 기대 수준이 서로 다름

같은 지표를 사용한다 하더라도 서로 판단 방식이 달라서 적정 주가를 서로 다르게 판단 => 매매 발생

한쪽 포지션으로만 몰리면 거래가 이뤄질리가...

##### valuation : 적정 주가 산출

Analyst : 경영전략, 시장 동향, 경쟁사 동향 등의 기업 활동 심층 분석 => 다양한 valuation 방법 적용하여 목표 주가 산정
          
\>>>> 종목마다 방법이 다름 => 만능키는 없다

Analyst가 사용하는 valuation model : DOM, Gordon의 성장모형, CAPM, FV/EBITDA, PER, EPS, PBR 등

finance engineering valuation : Quant traing 분야 => 유사한 다수 종목의 주가를 관찰해 주가를 형성하는 규칙을 발견하여 적정 주가 예측 => 통계학에 뿌리

##### 주가 비교의 첫걸음 : 비교 대상의 표준화

삼성전자와 주가비교를 위해 반도체라는 공통점이 있는 SK하이닉스와 전자라는 공통점이 있는 LG전자로 비교

먼저 하이닉스 그래프 

![useful image]({{ site.url }}/assets/images/hynix_stock_graph.png)

LG전자 그래프

![useful image]({{ site.url }}/assets/images/lg_electronic_stock_graph.png)

삼성과 하이닉스 LG중 수익률이 가장 높은 종목은? ~~어차피 난 셋다 없어 ㅠㅠ~~

따로 따로 보면 눈대중으로 파악이 힘들어진다.

그래서 삼성 하이닉스 LG의 그래프를 겹쳐보자

![useful image]({{ site.url }}/assets/images/samsung_lg_hynix_graph.png)

주가 수준이 다르므로 lg와 하이닉스는 오르는지 내리는지 알수가 없다. 

비율로 기준을 맞춰야 한다. => indexing(지수화)

$$Price_Index = {Price_{i} \over Price_{0}} \times Standard_Price$$

ex ) 기준일 : 2016년 1월 4일 / 기준가 : 100

| 일자 | SK하이닉스 | 삼성전자 | LG전자 |
| :---: | :---: | :---: | :---: |
| 2015-12-30 | 30,346 | 1,232,071 | 53,377 |
| 2016-01-04 | 29,754 | 1,178,290 | 52,087 |
| 2016-01-06 | 30,196 | 1,181,224 | 53,873 |

 1월 4일 종가기준으로 1월 5일의 index는 $$Price_Index = {Price_{i} \over Price_{0}} \times Standard_Price = {1,181,224 \over 1,178,290} \times 100 = 100.25$$

이 개념은 주가지수 산출, 편드 가격 산정 등에 동일하게 적용

이런식으로 indexing을 하면 그래프는

![useful image]({{ site.url }}/assets/images/samsung_lg_hynix_index.png)

상승률 

SK하이닉스 : 250%
삼성전자 : 210%
LG전자 : 200%

하이닉스가 가장 높은 상승률을 보인 것을 알 수 있다.

 

