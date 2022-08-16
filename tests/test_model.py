from model import Model


def test_model():
    model = Model()
    [model.add_image(f'.\\{i}.bmp') for i in range(1, 6)]
    assert model.images['1.bmp']
    assert model.folder == '.\\'
