# pinaca-python-sdk
Pinaca Labs' Python SDK

***Installation***

```bash
pip install --upgrade pinaca
```

***Translation***
```python
from pinaca import Translation
# TRANSLATION_URL, TRANSLATION_PASSWORD, TRANSLATION_USERNAME environment variables
# can be used without the need of passing the credentials as arguments to Translation
translation = Translation("https://gputwo.pinacalabs.com/translation/cn_en/sync", "USERNAME", "PASSWORD")

# Translating single texts
input_text = "就上述四人的年龄来看，郭和平年龄最大，系50后；庞建军、赵宾方为70后；张志兵为60后。"

translation_id = translation.run(input_text)

# Returns string
translated_text = translation.get_result(translation_id)

# Translating multiple texts at once
input_texts = ["就上述四人的年龄来看，郭和平年龄最大，系50后；庞建军、赵宾方为70后；张志兵为60后。",
                "资料显示，壶化股份2020年9月22日登陆A股市场，至今不足一年时间。据壶化股份彼时披露的招股书显示"]

translation_id = translation.run(input_texts)

# Returns list of strings
translated_texts = translation.get_result(translation_id)


```


