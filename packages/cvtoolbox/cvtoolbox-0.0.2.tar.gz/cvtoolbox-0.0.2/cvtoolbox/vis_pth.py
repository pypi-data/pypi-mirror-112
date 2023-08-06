import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.onnx
 
import netron
 
 
class model(nn.Module):
    def __init__(self):
        super(model, self).__init__()
        self.block1 = nn.Sequential(
            nn.Conv2d(64, 64, 3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 32, 1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 64, 3, padding=1, bias=False),
            nn.BatchNorm2d(64)
        )
 
        self.conv1 = nn.Conv2d(3, 64, 3, padding=1, bias=False)
        self.output = nn.Sequential(
            nn.Conv2d(64, 1, 3, padding=1, bias=True),
            nn.Sigmoid()
        )
 
    def forward(self, x):
        x = self.conv1(x)
        identity = x
        x = F.relu(self.block1(x) + identity)
        x = self.output(x)
        return x
 
 
d = torch.rand(1, 3, 416, 416)
m = model()
o = m(d)
 
onnx_path = "onnx_model_name.onnx"
torch.onnx.export(m, d, onnx_path)
 
netron.start(onnx_path)

# if __name__ == '__main__':
#     # os.environ['CUDA_VISIBLE_DEVICES']='0'
#     checkpoint = '/home/xds/Documents/model/resnet50-19c8e357.pth'
#     onnx_path = '/home/xds/Documents/model/resnet50-19c8e357.onnx'
#     dummy_input = torch.randn(1, 3, 1920, 1080)
#     # device = torch.device("cuda:2" if torch.cuda.is_available() else 'cpu')
#     # pth_to_onnx(input, checkpoint, onnx_path) 
#     model = torch.load(checkpoint)
#     model.load_state_dict(load(model_path, map_location='cpu')["model"])
#     torch.onnx._export(model, dummy_input, onnx_path, verbose=True, opset_version=11)