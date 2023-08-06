# TFReecord

> Read & Write TFRecord without heavy Tensorflow.

```bash
pip3 install tfreecord
```

## Example

### Write TFRecord

```python
import tfreecord

writer = tfreecord.RecordWriter()
feature = {
    'id': writer.int64_feature(759),
    'text': writer.bytes_feature("Now rides our knight".encode("utf-8")),
    'label': writer.bytes_feature("poem".encode("utf-8")),
}

with open("poems.tfrecord", "ab") as f:
    f.write(writer.encode_example(feature))
```

### Read TFRecord

```python
import tfreecord

reader = tfreecord.RecordReader()

for data in reader.read_from_tfrecord("poems.tfrecord"):
    print(data)
```

Thanks to [Jong Wook Kim](https://jongwook.kim/) blog post about TFRecords [here](https://jongwook.kim/blog/Anatomy-of-TFRecord.html) and his [tfrecord_lite](https://github.com/jongwook/tfrecord_lite) library.
