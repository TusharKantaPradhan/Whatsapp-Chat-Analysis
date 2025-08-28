from scripts.chat_parser import parse_chat
import io

def test_parse_chat():
    sample = '12/12/2024, 10:15 PM - Alice: Hello!'
    df = parse_chat(io.BytesIO(sample.encode()))
    assert df.shape[0] == 1
    assert df.iloc[0]['user'] == 'Alice'
