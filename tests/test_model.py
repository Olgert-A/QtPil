from model import Model


def test_model():
    model = Model()
    [model.add(f'.\\{i}.bmp') for i in range(1, 6)]
    assert model.data['1.bmp']
    assert model.folder == '.\\'
