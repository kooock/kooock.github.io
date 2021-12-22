---
layout: post
title: Why Transformers are Slowly Replacing CNNs in Computer Vision? 번역
excerpt: "Just about everything you'll need to style in the theme: headings, paragraphs, blockquotes, tables, code blocks, and more."
modified: 2021-12-22
tags: [computer vision, CNN, ViT, ConViT]
comments: true
---

# Why Transformers are Slowly Replacing CNNs in Computer Vision? 번역


**By:** [Pranoy Radhakrishnan](https://in.linkedin.com/in/pranoy-radhakrishnan-63846888)

이 글은 [Pranoy Radhakrishnan](https://in.linkedin.com/in/pranoy-radhakrishnan-63846888)가 [Medium 블로그에 작성한 글](https://becominghuman.ai/transformers-in-vision-e2e87b739feb)을 임의로 번역한 것입니다.

# Why Transformers are Slowly Replacing CNNs in Computer Vision?

Transformer에 들어가기 앞서, 왜 연구자들이 MLP나 CNN, RNN 같은 것들이 있음에도 불구하고 transformer와 같은 모델을 구성하는지 이해할 필요가 있습니다.

- transformer는 원래 언어번역을 수행하기 위해 설계되었습니다. transformer는 LSTM같은 RNN류와 비교했을 때, 인풋 시퀀스 요소들 간의 긴 의존성을 모델링할 수 있고 병렬처리를 지원합니다.
- transformer의 직관적인 디자인은 멀티 모달리티(멀티 테스크: 이미지, 비디오, 텍스트 음성)를 유사한 블록을 사용해서 처리할 수 있게 합니다.

모두가 단 하나의 보편적인 모델을 사용해서 여러 테스크의 문제를 정확도와 속도를 유지한 채로 풀고싶어 합니다. 범용 function approximator(함수에 근사시키는 것)인 MLP와 마찬가지로 transformer 모델은 sequence to sequence 함수에 대한 보편적인 approximator입니다.

transformer는 어텐션 메커니즘의 개념을 사용합니다. 어텐션이 무엇인지 알아보고 셀프 이텐션 메커니즘을 간략히 알아봅시다.

# Attention Mechanism

어텐션 메커니즘은 입력 데이터의 중요한 부분을 강화시키고 나머지 부분을 페이드아웃 시킵니다. 이미지를 캡셔닝하는 task를 수행한다고 가정해봅시다. 여러분은 의미있는 캡션을 생성하는데 관계있는 이미지의 부분을 주목해야 할 것입니다. 이것이 어텐션 메커니즘이 동작하는 방식입니다.

여기서 왜 우리는 어텐션이 필요할까요 CNN도 특징 추출에서는 꽤 성능이 좋잖아요?

![Untitled]({{ site.url }}/assets/images/20211222_01_000.png)


CNN의 경우에는 두 이미지가 거의 같습니다. CNN은 서로 다른 feature끼리의 상대위치를 인코딩 하지 못합니다. 이러한 feature의 조합을 인코딩 하기 위해서는 큰 필터들이 필요합니다. 예를 들어 “코와 입 위에 있는 눈”이라는 정보를 인코딩 하려면 큰 필터들이 필요해집니다.

이미지 내에서  **long-range dependencies(광범위 종속성)**를 추적하려면 **Large receptive fields(큰 수용 필드)가 필요합니다.** convolution kernel의 크기 증가는 네트워크의 표현능력을 증가시킬 수 있으나 동시에 local convolution 구조에서 얻을 수 있는 컴퓨팅 및 통계 효율이 사라져버립니다.

어텐션 메커니즘의 일종인 셀프 어텐션 모듈은 CNN과 함께 long-range dependencies를 컴퓨팅 및 통계 효율에 손상을 주지 않고 모델링하는데 도움이 됩니다.

![Self attention module used for SAGAN](https://miro.medium.com/max/700/1*3_SWBQ8gEbnXhhEWjlDGYg.png)

Self attention module used for SAGAN

여기 셀프 어텐션이 컨볼루션 레이어를 대체하는 것을 볼 수 있습니다. 이제 이 모델은 그 위치에서 멀리 떨어진 픽셀과도 상호작용 할 수 있는 능력을 얻게 되었습니다.

> 최근에는, 연구자들이 ResNets의 컨볼루션 레이어 일부 또는 전체를 attention으로 바꾸는 일련의 실험을 수행하였습니다. 그리고 최적의 성능을 내는 앞부분은 컨볼루션 레이어로 뒷부분은 attention 레이어를 이용한 모델을 찾았습니다.
> 

## Self Attention

셀프 어텐션 메커니즘은 **시퀀스의 모든 요소가 다른 모든 요소와 상호작용 할 수 있게 하고 어떤 요소에게 더 주의를 기울여야 하는지를 알아낼 수 있도록 하는** 일종의 어텐션 메커니즘입니다.

![셀프어텐션의 목적은 모든 n개의 엔티티 사이의 상호작용을 포착하는 것입니다. 셀프어텐션은 **다른 모든 워드 임베딩의 가중치 조합**입니다.](https://miro.medium.com/max/262/0*tJ9-TGWeMqCj-Xmk.png)

셀프어텐션의 목적은 모든 n개의 엔티티 사이의 상호작용을 포착하는 것입니다. 셀프어텐션은 **다른 모든 워드 임베딩의 가중치 조합**입니다.

이것은 ‘long-term’  정보와 시퀀스 요소 간의 종속성을 포착할 수 있습니다.

위의 이미지에서 알 수 있듯이, “it”은 “street”을 참조하고 “animal”하고는 딱히 관계가 없습니다. 셀프 어텐션은 다**른 모든 워드 임베딩의 가중치 조합**입니다. **여기 “it”의 임베딩은 “street”이라는 단어에 더 많은 가중치가 있는 모든 임베딩 벡터의 가중치 조합입니다.**

가중치를 어떻게 주는지를 이해하려면 이걸 시청하세요— [https://www.youtube.com/watch?v=tIvKXrEDMhk](https://www.youtube.com/watch?v=tIvKXrEDMhk)

기본적으로 셀프 어텐션 레이어는 **전체 입력 시퀀스에서 전역 정보를 aggregating**하여 시퀀스의 각 컴포넌트를 업데이트합니다.

우리는 지금까지 셀프 어텐션과 같은 어텐션 메커니즘이 어떻게 효율적으로 컨볼루션 네트워크의 한계를 해결했는지 알아왔습니다. 그럼 이제 transformer와 같은 어텐션 기반 모델이 CNN을 완전히 대체하는게 가능할까요?

transformer는 이미 NLP 도메인에서  LSTM을 대체하였습니다. 그렇다면 transformer가 컴퓨터 비전의 CNN을 대체할 수 있는 가능성은 무엇일까요. CNN의 성능을 능가하는 어텐션을 기반으로 구축된 접근방식은 무엇일까요. 지금부터 같이 보도록 합시다.

# The Transformer Model

![https://miro.medium.com/max/700/0*6IRI1702tSRvY04a.png](https://miro.medium.com/max/700/0*6IRI1702tSRvY04a.png)

transformer 모델은 NLP task에서 중요한 기계번역 문제를 해결하기 위해 최초로 제안되었습니다. 이때 제안된 transformer 모델은 인코더 디코더 구조를 가집니다. 위 사진에서 왼쪽은 인코더 오른쪽은 디코더를 나타냅니다. 보시는 것과 같이 인코더와 디코더 모두 셀프 어텐션 레이어와 션형 레이어, residual connection을 가집니다.

<aside>
💡 Note: 컨볼루션 네트워크에서, feature aggregation과 feature transformation이 동시에 수행됩니다.(예를 들어 비선형 함수가 뒤에 있는 컨볼루션 레이어) 이것을 transformer 모델에서는 두 단계로 나눠서 수행합니다. 예를 들어 셀프 어텐션 레이어에서 aggregation만을 수행하고 feed-forward layer는 transformation만을 수행합니다.

</aside>

## The encoder

언어 변환의 경우를 봅시다. 인코더의 셀프 어텐션 메커니즘은 인풋의 워드들이 서로 다른 워드들과 상호작용을 할 수 있게 해줘서 다른 토큰들과 의미론적 유사성을 가지는 각 토큰에 대한 표현을 생성하도록 합니다.

## The Decoder

디코더가 하는 일은 입력 임베딩과 지금까지 생성된 아웃풋 모두를 어텐딩하여 한번에 하나씩 번역된 단어를 출력하는 것입니다.

디코더는 인코더 출력의 특정 부분에 집중하고 지금까지 생성된 이전 아웃풋을 봄으로써 한번에 하나의 단어를 출력합니다. 학습시에 디코더가 미래의 아웃풋을 보지 않고 오직 과거에 생성된 아웃풋 만을 보는 것을 보장하기 위해 마스크 셀프 어텐션 메커니즘을 디코더에 사용합니다. 이는 학습시에 디코더의 인풋으로 주어지는 미래의 단어를 마스킹합니다.

셀프 어텐션은 위치를 신경쓰지 않습니다. 예를 들어 “Deepak is the son of Pradeep”이라는 문장이 있습니다. 셀프 어텐션은 “son”에 대하여 “Deepak”에 가중치를 더 준다고 생각해봅시다. 만약에 이 문장을 섞는다면, “Pradeep is the son of Deepak” 이렇게 되는데 셀프 어텐션은 여전히 “son”에 대하여 “Deepak”에 가중치를 더 줍니다. 하지만 이제 우리는 셀프텐션이 “son”에 대하여 “Pradeep”에 가중치를 더 주길 원합니다.

이런 문제의 원인은 셀프 어텐션 모듈이 **“son”을 위치정보를 고려하지 않고 모든 단어 임베딩의 weighted combination로 인코딩하기 때문입니다.** 그래서 토큰을 섞어버리면 차이를 만들어내지 못합니다. 다른말로는 셀프 어텐션은 permutation invariant(순열 불변)하다고 합니다. 셀프 어텐션은 여러분이 임베딩을 셀프 어텐션 모듈로 전달 하기 전에 위치 정보를 토큰에다가 집어넣지 않는 한 permutation invariant입니다.

### Positional Encoding

(이 부분은 원본에는 없으나 설명이 부족한 것 같아서 역자가 추가한 내용입니다.)

 이런 위치정보를 토큰에 집어넣기 위해서 positional encoding을 사용합니다. 맨 처음 가장 간단하게 생각할 수 있는 postional encoding은 그냥 자리마다 increasing number를 하나씩 주는 겁니다. 

![Untitled]({{ site.url }}/assets/images/20211222_01_001.png)

그 방식의 문제는 각 자리 토큰 간의 숫자가 너무 크게 차이가 나게 되어 학습시 gradient explosion등으로 학습이 불안정해질 수 있습니다. 그러면 0~1 사이로 normalizing 하면 되지 라고 생각할 수 있습니다. 

![Untitled]({{ site.url }}/assets/images/20211222_01_002.png)

그런데 문제가 같은 자리에는 같은 포지셔널 인코딩 값이 들어와야 하는건데 시퀀스 최대길이 값이 다르면 같은 자리인데도 다른 값을 받게 됩니다. 최대 길이 11인 시퀀스에서는 3번째 자리가 0.3이고 최대 길이가 6인 시퀀스에서는 3번째 자리가 0.6입니다.  그러면 이런 문제를 해결하기 위해서 바이너리 백터를 이용한다면 일정한 자리마다 고유값을 부여할 수 있습니다. 

![Untitled]({{ site.url }}/assets/images/20211222_01_003.png)

하지만 이 방식의 문제는 이산적 함수의 출력이기에 (0,0) ~ (0,1) 사이의 거리는 1인데 (0,1) ~ (1,0) 사이의 거리는 루트2로 각 자리 사이마다 거리가 달라지게 되어 버립니다. 하지만 각 자리가 거리의 차리를 주는 의미를 가져선 안되므로 문제가 됩니다. 이는 고차원으로 갈 수록 더욱 뚜렸해지는 문제입니다. 

그래서 연속적인 바이너리 백터를 찾아야만 했습니다. 0~1사이에서 움직이며 연속적이고 frequency의 차이로 인코딩을 할 수 있는 것은 sin입니다. 

![Untitled]({{ site.url }}/assets/images/20211222_01_004.png)

이렇게 했을때의 문제는 dim3의 경우 반바퀴를 돌면 제자리로 돌아오는데 반바퀴를 돈 경우와 첫번째 스텝의 거리가 매우 가까워집니다. 즉 같은 자리에서 순환하는 닫힌 형태인데 이렇게 되면 마지막 자리와 첫번째 자리가 가까워져버리는 문제가 발생합니다. 그리고 또 한가지 문제는 스텝 인덱스에 따른 positional encoding 변환을 반영하지 못한다는 것인데 즉 다른 인덱스로부터의 선형변환으로써 표현되지 못한다는 의미입니다. $$PE(x + \nabla x) = PE(x)\cdot T(\nabla x)$$  **를 만족시켜야 하는데 만족시킬 수 있는 $$T(\nabla x)$$가 없다는 것입니다.  이 문제는 회전변환에서 아이디어를 얻어서 해결합니다. 

![Untitled]({{ site.url }}/assets/images/20211222_01_005.png)

이렇게 얻어진 $$PE(x)$$ 행렬을 sin과 cos함수를 번갈아가면서  구성합니다.

![Untitled]({{ site.url }}/assets/images/20211222_01_006.png)

그리고 선형변환 $$T(\nabla x)$$ 는 다음과 같이 구성이 가능합니다.

![Untitled]({{ site.url }}/assets/images/20211222_01_007.png)

![Untitled]({{ site.url }}/assets/images/20211222_01_008.png)

# Vision Transformer

![Vision Transformer](https://miro.medium.com/max/642/0*g3USe8h3x92w0pRd.png)

Vision Transformer

vision transformer는 컨볼루션을 완전히 transformer로 대체하는 접근입니다. 

Transformer always operates on sequences, thats why we split the images to patches and and flattening each such “patch” to a vector. From now i would call a “patch” as a token. So now have a sequence of tokens.

trnasformer는 항상 스퀀스에 대한 동작만 합니다. 이것이 바로 우리가 이미지를 patches로 쪼갠 후에 그것을 flattening해서 vector로 만든 이유입니다. 지금부터 우리는 “patch”를 토큰으로 부를 겁니다. 그러면 이제 우리는 토큰들의 시퀀스를 가질 수 있게 됩니다.

셀프 어텐션은 **permutation invariant** 하게 설계되어 있습니다. 셀프 어텐션은 서로 다른 어텐션 벡터의 가중합을 수행할 때 합산 연산을 “일반화”힙니다. 

순열에 따른 불변성이라는 것은 먄약에 [A, B, C, D] 라는 인풋이 있다고 한다면 네트워크는 [A, C, B, D]라고 하는 인풋 또는 이와 같은 다른 순열에도 같은 결과를 내보낸다는 의미입니다.

(저자가 똑같은 말을 계속 반복하는 듯한 느낌이 듭니다. 아니 그렇게 이게 중요하면 positional encoding을 제대로 본문에 설명해야 하는 거 아닌가라는 생각 또한 듭니다.)

So positional information is added to each token before passing the whole sequence to the self attention module. Adding positional information will help the transformer understand the relative position of each tokens in the sequence. Here positional encodings are learned instead of using standard encodings.

위치정보는 전체 시퀀스가 셀프어텐션 모듈을 거치기 전에 각 토큰에 추가됩니다. 위치정보의 추가는 시퀀스에서 각 토큰의 상대적 위치를 transformer가 이해하는데 도움을 줍니다. 여기에서 standard 인코딩을 사용하는 대신 positional encoding을 학습합니다.(여기서 학습은 기계가 아니라 이 블로그를 보는 우리 휴먼들이 하는 겁니다. train이 아니라 learned를 번역한겁니다. positional encoding은 기계가 학습해서 맞춰지는 개념이 절대 아닙니다.)

![positional encoding을 추가하지 않으면 transformer 두 이미지의 시퀀스를 동일하게 봅니다.](https://miro.medium.com/max/700/1*0d7JFm5NiyqJiq3XdeFXNw.png)

positional encoding을 추가하지 않으면 transformer 두 이미지의 시퀀스를 동일하게 봅니다.

Finally output of the transformer from the first position is used for further classification by an MLP.

마지막으로 첫번째 위치의 transformer 출력은 MLP에 의해서 classification에 사용됩니다.

transformer의 학습은 CNN보다 더 많은 데이터가 필요합니다. 그 이유는 CNN은 translational equivariance과 같은 이미지 도메인에 대한 사전 지식을 인코딩합니다. 반면에 transformer는 주어진 데이터 만으로 이를 배워야 합니다.

Translational equivariance는 우리 오브젝트를 이미지의 오른쪽으로 이동했을 때, feature layer의 활성도가 오른쪽으로 이동하는 컨볼루션 레이어의 속성입니다.

# ConViT

vistion transformer는 pixel patch 전체에 걸쳐 셀프 어텐션을 수행함으로써 convolutional의 inductive bias(예: equivariance)를 완전하게 제공합니다. 이것의 단점은 처음에 모든 것을 학습하기 위해 많은 양의 데이터를 요구합니다.

CNN은 hard inductive bias 때문에 적은 데이터에서는 더 나은 성능을 보입니다. 많은 양의 데이터를 사용할 수 있는 경우에는, (CNN에게서 부여받은)hard inductive bias는 모델의 전체 능력을 제한합니다.

그렇다면 대용량 데이터 영역의 한계에서 곶통받지 않고 낮은 데이터 영역에서 CNN의 hard inductive bias의 혜택을 얻을 수 있는게 가능한가?

이것에 대한 아이디어는 필요한 경우 모델이 convolution layer로 작동할 수 있도록 하는 Positinal self attention(PSA) 메커니즘을 도입하는 것입니다. 우리는 단지 셀프 어텐션 레이어의 일부를 PSA 플레이어로 교체하는 것입니다.

우리는 셀프 어텐션이 permutation invariant이기 때문에 위치정보가 항상 patch에 추가된다는 것을 알 수 있습니다. (VIT처럼)셀프 어텐션 레이어를 통과하여 다음 레이어로 순전파하기 전에 임베딩 타임에 입력에 위치 정보를 추가하는 것 대신 우리는 vanilla self attention를 PSA로 대체합니다.

(아 이거 때문에 positional encoding에 대한 구체적인 설명 없이 positional information의 중요성에 대해서 그렇게 반복했던 거군요! 필자의 큰그림에 역자는 부...아니 무릎을 탁 치고 갑니다)

PSA에서 우리는 어텐션 가중치가 **relative positional encodings(r)**과 **trainable embedding(v)** 로 계산된다는 것을 알 수 있습니다. Relative positional encodings(r)는 오직 픽셀간의 거리에만 의존합니다.

![https://miro.medium.com/max/313/1*SSdJYIx4W5hbdoO-bJt-fw.png](https://miro.medium.com/max/313/1*SSdJYIx4W5hbdoO-bJt-fw.png)


학습가능한 **positional encoding이 있는** 멀티 헤드 PSA 레이어는 모든 컨볼루션 레이어를 표현할 수 있습니다.

따라서 우리는 어텐션 메커니즘과 CNN을 결합하지 않습니다. 그 대신 우리는 일부 파라미터를 조정하여 convolution으로 작동할 수 있게 하는 PSA 레이어를 사용합니다. 우리는 초기화 시 PSA 레이어의 이 능력을 활용합니다. 소규모 데이터 영역에서 이는 모델이 일반화되는 데 도움이 될 수 있습니다. 반면에 대규모 데이터 영역에서 PSA 레이어는 필요한 경우 컨볼루션의 특성을 남길 수 있습니다.

# Conclusion

우리는 원래 기계번역 문제를 해결하기 위해서 개발된  transformer가 컴퓨터 비전분야에 좋은 결과를 보여주고 있음을 보여줍니다. 이미지 분류에서 CNN을 능가하는 ViT는 중요한 돌파구였습니다. 그러나 대규모 외부 데이터셋에 대한 비용이 많이 드는 pre-training이 필요합니다. ConViT는 imageNet에서 ViT를 능가하는 동시에 훨씬 향상된 샘플 효율성을 제공합니다 이러한 결과는 transformer가 많은 컴퓨터 비전 작업에서 CNN을 추월할 수 있음을 보여줍니다.

# References

Transformers in Vision — [https://arxiv.org/pdf/2101.01169.pdf](https://arxiv.org/pdf/2101.01169.pdf)

ConViT — [https://arxiv.org/pdf/2103.10697.pdf](https://arxiv.org/pdf/2103.10697.pdf)
