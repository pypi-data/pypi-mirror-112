# transformers-keras

![Python package](https://github.com/luozhouyang/transformers-keras/workflows/Python%20package/badge.svg)
[![PyPI version](https://badge.fury.io/py/transformers-keras.svg)](https://badge.fury.io/py/transformers-keras)
[![Python](https://img.shields.io/pypi/pyversions/transformers-keras.svg?style=plastic)](https://badge.fury.io/py/transformers-keras)

[English](README_EN.md) | 中文文档 

基于`tf.keras`的Transformers系列模型实现。

# 目录
1. [安装](#安装)
2. [实现的模型](#实现的模型)
3. [BERT](#BERT)
    - 3.1 [BERT支持的预训练权重](#BERT)
    - 3.2 [BERT特征抽取示例](#BERT特征抽取示例)
    - 3.3 [BERT微调模型示例](#BERT微调模型示例)
    - 3.4 [BERT模型导出和部署](#BERT导出SavedModel格式的模型用Serving部署)
4. [ALBERT](#ALBERT)
    - 4.1 [ALBERT支持的预训练权重](#ALBERT)
    - 4.2 [ALBERT特征抽取示例](#ALBERT特征抽取示例)
    - 4.3 [ALBERT微调模型示例](#ALBERT微调模型示例)
    - 4.4 [ALBERT模型导出和部署](#ALBERT导出SavedModel格式的模型用Serving部署)
5. [进阶使用](#进阶使用)
    - 5.1 [加载时跳过一些参数的权重](#加载预训练模型权重的过程中跳过一些参数的权重)
    - 5.2 [加载第三方模型实现的权重](#加载第三方实现的模型的权重)


## 安装

```bash
pip install -U transformers-keras
```

## 实现的模型

- [x] Transformer[*已删除*]
  * [Attention Is All You Need](https://arxiv.org/abs/1706.03762). 
  * TensorFlow官方教程:[Transformer model for language understanding](https://www.tensorflow.org/beta/tutorials/text/transformer)
- [x] BERT
  * [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)
- [x] ALBERT
  * [ALBERT: A Lite BERT for Self-supervised Learning of Language Representations](https://arxiv.org/abs/1909.11942)


## BERT

支持加载的预训练BERT模型权重:

* 所有使用 [google-research/bert](https://github.com/google-research/bert) 训练的**BERT**模型
* 所有使用 [ymcui/Chinese-BERT-wwm](https://github.com/ymcui/Chinese-BERT-wwm) 训练的**BERT**和**RoBERTa**模型

### BERT特征抽取示例

```python
from transformers_keras import Bert

# 加载预训练模型权重
model = Bert.from_pretrained('/path/to/pretrained/bert/model')
input_ids = tf.constant([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
# segment_ids and attention_mask 是可选的
sequence_outputs, pooled_output = model(input_ids, training=False)

```

另外，可以通过构造器参数 `return_states=True` 和 `return_attention_weights=True` 来获取每一层的 `hidden_states` 和 `attention_weights` 输出:

```python
from transformers_keras import Bert

# 加载预训练模型权重
model = Bert.from_pretrained(
    '/path/to/pretrained/bert/model', 
    return_states=True, 
    return_attention_weights=True)
input_ids = tf.constant([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
# segment_ids and attention_mask 是可以选的
sequence_outputs, pooled_output, hidden_states, attn_weights = model(input_ids, training=False)

```

### BERT微调模型示例

```python
# 构建一个简单的二分类模型
def build_bert_classify_model(pretrained_model_dir, **kwargs):
    input_ids = tf.keras.layers.Input(shape=(None,), dtype=tf.int32, name='input_ids')
    # segment_ids and attention_mask 是可选的
    segment_ids = tf.keras.layers.Input(shape=(None,), dtype=tf.int32, name='segment_ids')
    # 加载预训练模型权重
    bert = Bert.from_pretrained(pretrained_model_dir, **kwargs)

    sequence_outputs, pooled_output = bert(input_ids, segment_ids)
    outputs = tf.keras.layers.Dense(2, name='output')(pooled_output)
    model = tf.keras.Model(inputs=[input_ids, segment_ids], outputs=outputs)
    model.compile(loss='binary_cross_entropy', optimizer='adam')
    return model

model = build_bert_classify_model(
            pretrained_model_dir=os.path.join(BASE_DIR, 'chinese_wwm_ext_L-12_H-768_A-12'),
        )
model.summary()
```

### BERT导出SavedModel格式的模型用Serving部署

你可以很方便地把模型转换成SavedModel格式。这里是一个示例:

```python
# 加载预训练模型权重
model = Bert.from_pretrained(
    '/path/to/pretrained/bert/model', 
    return_states=True, 
    return_attention_weights=True)
# 导出SavedModel格式的模型, model.serving 定义了模型的输入输出
model.save('/path/to/save', signatures=model.serving)
```

接下来，就可以使用 [tensorflow/serving](https://github.com/tensorflow/serving) 来部署模型了。


## ALBERT

支持加载的预训练ALBERT模型权重:

* 所有使用 [google-research/albert](https://github.com/google-research/albert) 训练的模型。

### ALBERT特征抽取示例

```python
from transformers_keras import Albert

# 加载预训练权重
model = Albert.from_pretrained('/path/to/pretrained/albert/model')
input_ids = tf.constant([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
# segment_ids and attention_mask 是可选的
sequence_outputs, pooled_output = model(input_ids, training=False)
```

另外，可以通过构造器参数 `return_states=True` 和 `return_attention_weights=True` 来获取每一层的 `hidden_states` 和 `attention_weights` 输出:

```python
from transformers_keras import Albert

# 加载预训练模型权重
model = Albert.from_pretrained(
    '/path/to/pretrained/albert/model', 
    return_states=True, 
    return_attention_weights=True)

input_ids = tf.constant([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
# segment_ids and attention_mask 是可选的
sequence_outputs, pooled_output, states, attn_weights = model(input_ids, training=False)
```

### ALBERT微调模型示例

```python

# Used to fine-tuning 
def build_albert_classify_model(pretrained_model_dir, **kwargs):
    input_ids = tf.keras.layers.Input(shape=(None,), dtype=tf.int32, name='input_ids')
    # segment_ids and attention_mask are optional
    segment_ids = tf.keras.layers.Input(shape=(None,), dtype=tf.int32, name='segment_ids')

    albert = Albert.from_pretrained(pretrained_model_dir, **kwargs)

    sequence_outputs, pooled_output = albert(input_ids, segment_ids)
    outputs = tf.keras.layers.Dense(2, name='output')(pooled_output)
    model = tf.keras.Model(inputs=[input_ids, segment_ids], outputs=outputs)
    model.compile(loss='binary_cross_entropy', optimizer='adam')
    return model

model = build_albert_classify_model(
            pretrained_model_dir=os.path.join(BASE_DIR, 'albert_base'),
        )
model.summary()
```


### ALBERT导出SavedModel格式的模型用Serving部署

你可以很方便地把模型转换成SavedModel格式。这里是一个示例:

```python
# 加载预训练模型权重
model = Albert.from_pretrained(
    '/path/to/pretrained/albert/model', 
    return_states=True, 
    return_attention_weights=True)
# 导出SavedModel格式的模型, model.serving 定义了模型的输入输出
model.save('/path/to/save', signatures=model.serving)
```

接下来，就可以使用 [tensorflow/serving](https://github.com/tensorflow/serving) 来部署模型了。


## 进阶使用

支持的高级使用方法:

* 加载预训练模型权重的过程中跳过一些参数的权重
* 加载第三方实现的模型的权重

### 加载预训练模型权重的过程中跳过一些参数的权重

有些情况下，你可能会在加载预训练权重的过程中，跳过一些权重的加载。这个过程很简单。

这里是一个示例：

```python
from transformers_keras import Bert, Albert

ALBERT_MODEL_PATH = '/path/to/albert/model'
albert = Albert.from_pretrained(
    ALBERT_MODEL_PATH,
    # return_states=False,
    # return_attention_weights=False,
    skip_token_embedding=True,
    skip_position_embedding=True,
    skip_segment_embedding=True,
    skip_pooler=True,
    ...
    )

BERT_MODEL_PATH = '/path/to/bert/model'
bert = Bert.from_pretrained(
    BERT_MODEL_PATH,
    # return_states=False,
    # return_attention_weights=False,
    skip_token_embedding=True,
    skip_position_embedding=True,
    skip_segment_embedding=True,
    skip_pooler=True,
    ...
    )
```

所有支持跳过加载的权重如下:

* `skip_token_embedding`, 跳过加载ckpt的 `token_embedding` 权重
* `skip_position_embedding`, 跳过加载ckpt的 `position_embedding` 权重
* `skip_segment_embedding`, 跳过加载ckpt的 `token_type_emebdding` 权重
* `skip_embedding_layernorm`, 跳过加载ckpt的 `layer_norm` 权重
* `skip_pooler`, 跳过加载ckpt的 `pooler` 权重



### 加载第三方实现的模型的权重

在有一些情况下，第三方实现了一些模型，它的权重的结构组织和官方的实现不太一样。对于一般的预训练加载库，实现这个功能是需要库本身修改代码来实现的。本库通过 **适配器模式** 提供了这种支持。用户只需要继承 **AbstractAdapter** 即可实现自定义的权重加载逻辑。

```python
from transformers_keras.adapters import AbstractAdapter
from transformers_keras import Bert, Albert

# 自定义的BERT权重适配器
class MyBertAdapter(AbstractAdapter):

    def adapte_config(self, config_file, **kwargs):
        # 在这里把配置文件的配置项，转化成本库的BERT需要的配置
        # 本库实现的BERT所需参数都在构造器里，可以简单方便得查看
        pass

    def adapte_weights(self, model, config, ckpt, **kwargs):
        # 在这里把ckpt的权重设置到model的权重里
        # 可以参考BertAdapter的实现过程
        pass

# 加载预训练权重的时候，指定自己的适配器 `adapter=MyBertAdapter()`
bert = Bert.from_pretrained('/path/to/your/bert/model', adapter=MyBertAdapter())

# 自定义的ALBERT权重适配器
class MyAlbertAdapter(AbstractAdapter):

    def adapte_config(self, config_file, **kwargs):
        # 在这里把配置文件的配置项，转化成本库的BERT需要的配置
        # 本库实现的ALBERT所需参数都在构造器里，可以简单方便得查看
        pass

    def adapte_weights(self, model, config, ckpt, **kwargs):
        # 在这里把ckpt的权重设置到model的权重里
        # 可以参考AlbertAdapter的实现过程
        pass

# 加载预训练权重的时候，指定自己的适配器 `adapter=MyAlbertAdapter()`
albert = Albert.from_pretrained('/path/to/your/albert/model', adapter=MyAlbertAdapter())
```
