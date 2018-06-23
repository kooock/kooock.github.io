---
layout: post
title: 논문 <Get To The Point : Summarization with Pointer-Generator Network> 변역 
excerpt: "Just about everything you'll need to style in the theme: headings, paragraphs, blockquotes, tables, code blocks, and more."
modified: 2018-06-21
tags: [딥러닝, 논문, 번역, 요약]
comments: true
---

### Get To The Point : Summarization with Pointer-Generator Network 번역
-----------------------------------------------------------------------------------------------

| Abigail See         | Peter J. Liu         | Christopher D. Manning | 
| :-----------------: | :------------------: | :--------------------: |
| Stanford University | Google Brain         | Stanford University    |
| abisee@stanford.edu | peterjliu@google.com | manning@stanford.edu   |


#### 초록
지금까지 글의 요약(원문의 단순한 단어 선택과 구절 재배열을 넘어서는 요약)을 위한 실행가능한 seq2seq 인공신경망 모델 설계방법들이 제안되어 왔다.
하지만, 이 모델들은 구체적으로 사실과 다르게 요약을 하거나 같은 단어를 반복하는 경향이 있다는 두자지 단점을 가지고 있다.
본 연구에서 우리는 두가지 상호직교하는 방법을 통한 standard seq2seq attentional 모델의 새로운 아키텍처를 제안한다.
첫번째 방법은 새로운 단어를 만들 수 있는 능력을 가지는 generator와 원문에서 단어를 복사하여 정확한 정보의 재생산에 도움을 주는 pointing을 결합한 하이브리드 형태의 pointer-generator 신경망을 사용하는 것이다.
두번째 방법은 반복을 피할 수 있도록 요약됐던 기록을 유지하는 coverage를 유지하는 것이다.
우리는 모델을 위의 모델을 적용하여 CNN과 Daily Mail를 요약하는 작업에서 기존의 2 ROUGE 포인트인 스테이츠오브아트 모델을 뛰어넘는 성능을 보여줬다.

#### 1. 소개
요약은 글뭉치를 원문의 주제가 포함된 짧은 글로 압축하는 작업이다. 이것은 크게 추출하는 방법과 추상화시키는 방법 두가지 방법이 있다. 
추출하는 방법은 전적으로 원문의 구절로부터 직접적으로 뽑아서 구성하는 것이다. 
반면에 추상화 방식은 사람이 요약하는 것과 유사하게 원문에 없던 새로운 단어와 구절을 만들어 낼 수 있다.
추출하는 방법은 비교적 쉬운데 원문에 있는 글의 각 부분을 복사하면 문법과 내용의 정확도가 기본적으로 확보되기 때문이다. 
바뀌서 생각하면 바뀌쓰기, 일반화하기 또는 실세계의 지식의 접목과 같이 높은 수준의 요약에 결정적인 정교한 능력들은 추상화 프레임워크에서만 가능하다.(그림 5 참초)

추상화 요약이 어렵기 때문에, 과거의 연구들은 추출식이 학계의 큰 주류를 이뤘다. 그리나 오늘날 recurrent neural networks(RNNs)의 일종으로 텍스트를 읽고 자유롭게 생성할 수 있는 seq2seq 모델(Sutskeveret al., 2014)의 성공은 추상화 요약을 실행가능하게 만들었다.(Chopraet al., 2016; Nallapati et al., 2016; Rush et al.,2015; Zeng et al., 2016)
그 시스템들이 장담했음에도 불구하고, 요약 시 사실적인 디테일을 잡아내지 못하거나, vocalbulary밖의 단어들을 다루지 못하고 같은 단어를 반복하는 등 그것들은 탐탁지 못한 결과를 보여줬다.(그림 1 참조)

본 논문에서는 다수의 문장 요약의 문맥에 있어서 세가지 이슈를 다루는 를 보여준다. 반면에 최근 추상하 요약 연구는 헤드라인(주제를 한두문장으로 줄인 것) 생성작업에 집중되어 있다.
우리는 긴 텍스트 요약이 더 도전가치(표현의 반복을 피하는 동시에 추상화의 난이도를 높히는 것)가 크고, 결국 더 유용하다고 생각한다. 
그러므로, 우리는 최근 소개된 뉴스기사(평균 39문장)와 여러문장의 요약이 쌍을 이루는 CNN/Daily Mail 데이터셋((Hermann et al., 2015; Nallap-ati et al., 2016))에 우리의 모델을 적용하고 가장 작은 2 ROUGE포인트로 기존의 스테이트오브아츠 추상화 시스템을 뛰어넘는 것을 보여준다.

우리의 하이브리드 pointer-generator 네트워크는 OOV단어어 처리와 정확도를 개선한 pointing(Vinyals et al., 2015)을 이용해서 원문의 단어를 복사하는 동시에 새로운 단어를 generate하는 능력을 유지하는 것을 용이하게 한다.
추출방식과 추상화 방식 사이에 균형을 보여줄 수 있는 이 네트워크는 짧은 글의 요약에 적용되는 Guet al.’s (2016)의 CopyNet과 Miao and Blunsom’s(2016)의 Forced-Attention Sentence Compression과 유사하다.
우리는 원문의 기록과 coverage의 제어를 이용하는 신경망 기계번역으로부터 새로운 coverage vector(Tu et al., 2016)의 변형을 제안한다.
우리는 coverage가 놀랍게도 표현의 반복을 제거하는 것에 효과적인 것을 밝힌다.

#### 2. 제안 모델
이 섹션에서 우리는 (1)기초가 되는 seq2seq모델과 (2)우리의 pointer-generator, 그리고 이 두 모델을 각각 추가할 수 있는 (3)우리의 coverage 메커니즘을 설명한다.
우리의 사용가능한 모델코드는 온라인으로 공개되었다.(www.github.com/abisee/pointer-generator)

##### 2.1. Sequence-to-sequence attentional model
우리의 기초모델은 Nallapati et al. (2016)와 유사하며 그림2에 설명되어 있다.
기사의 토큰들 \\(w_i\\)은 인코더의 히든 state \\(h_i\\)를 만드는 1대1 인코더(1층짜리 양방향 LSTM)에 입력된다.
각 스탭 \\(t\\)에서 디코더(한층짜리 단방향 LSTM)는 임베딩된 직전 단어(학습하는 동안 참조 요약의 직전 단어, 테스트때 디코더에서 나오는 직전 단어)를 받고 더코더 state \\(s_i\\)를 가진다.
attention distribution \\(a_t\\)는 Bahdanau et al. (2015)에서와 같이 계산되어진다.


\\(a_{i}^{t} = v^{T}tanh(W_{t}h{i} + W_{s}s_{t} + b_{attn})\\)      (1)
\\(a^{t} = softmax(e^{t})\\)                                        (2)


\\(v\\)에서 \\(W_h\\), \\(W_{s}\\)와 \\(b_{attn}\\)는 학습가능한 파라미터들이다.
attention distribution은  다음 단어를 만들어 낼 곳을 디코더에게 알려주는 원문 단어들의 확률분산으로 볼 수 있다.
다음으로, attention distribution은 context vector \\(h_{t}^{\ast}\\)로 알려진 인코더 히든 state들의 가중치 합의 결과로 다뤄진다.


\\(h_{t}^{\ast} = \sum_{i} a_{i}^{t}h_{i}\\)                           (3)


이 단계에서 원문에서 읽은 것을 고정된 사이즈로 표시한다고 볼 수 있는 context vector \\(e\\)는 디코드 state \\(s_{t}\\)와 연결되고 vocabulary distribution을 만들어내는 두층짜리 linear layer로부터 입력받는다.


\\(P_{vocab} = softmax(V'(V[s_{t},h_{t}^{\ast}]+b)+b')\\)              (4)


\\(V\\),\\(V'\\),\\(b\\)와 \\(b'\\)는 학습가능한 파라미터들이다.
\\(P_{vocab}\\)은 vocabulary의 모든 단어의 확률 분산이며 예측한 단어들 \\(w\\)의 최종적인 분산을 내타낸다.


\\(P(w) = P_{vocab}(w)\\)                                           (5)

학습하는 동안 타임스텝 \\(t\\) 에서의 손실함수는 해당 타임스텝에서의 타겟 단어 \\(w_{t}^{\ast}\\)의 음의 log likelyhood이다.


\\(loss_{t} = -log P(w_{t)^{\ast}\\)                                     (6)


그리고 전체 시퀀스에서의 통합 손실함수는 다음과 같다.


\\(loss = \frac{1}{T}\sum_{t=0}^{T} loss_{t}\\)                     (7)


##### 2.2. Pointer-generator network
우리의 pointer-generator network는 pointing에 의해 단어를 복사하고 고정된 vocabulary로부터 단어를 생성하기 위해 우리의 기초 seq2seq모델과 pointer network(Vinyals et al.,2015)의 하이브리드 형태이다.
Pointer-generator network 모델(그림 3에서 묘사된)에서 attention distribution \\(a^{t}\\)와 context vector \\(h_{t}^{\ast}\\)는 색션 2.1.과 같이 계산되어진다. 
덧붙히자면, 타임스텝 \\(t\\)에서의 generation probability P_{gen} \in [0,1])은 context vector \\(h_{t}^{\ast}\\), 디코더 state \\(s_{t}\\)와 디코더 입력값 \\(s_{t}\\)으로부터 계산되어진다.


\\(P_{gen} = \boldsymbol{\sigma}(w_{h^{\ast}}^{T}h_{t}^{\ast} + w_{s}^{T}s_{t} + w_{s}^{T}x_{t} + b_{ptr})\\)


vector들 \\(w_{h^{\ast}}\\),\\(\\)

