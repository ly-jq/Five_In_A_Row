import torch.nn.functional as F
import utils.config as cfg
import torch.nn as nn


def conv3x3(input,output):
    return  nn.Conv2d(input,output,3)

def bn2d(input):
    return nn.BatchNorm2d(input)

#残差快    same_shape表示是否在残差边上使用卷积层过滤
class ResnetBlock(nn.Module):
    def __init__(self, in_channel, out_channel, strides=1, same_shape=True):
        super(ResnetBlock, self).__init__()
        self.same_shape = same_shape
        if not same_shape:
            strides = 2
        self.strides = strides
        self.block = nn.Sequential(
            nn.Conv2d(in_channel, out_channel, kernel_size=3, stride=strides, padding=1, bias=False),
            nn.BatchNorm2d(out_channel),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channel, out_channel, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channel)
        )
        if not same_shape:
            self.conv3 = nn.Conv2d(in_channel, out_channel, kernel_size=1, stride=strides, bias=False)
            self.bn3 = nn.BatchNorm2d(out_channel)

    def forward(self, x):
        out = self.block(x)
        if not self.same_shape:
            x = self.bn3(self.conv3(x))
        return F.relu(out + x)

class PolicyValueNet(nn.Module):
    def __init__(self,conv_filters,resnet_filters,policy_filters,learning_rate=cfg.learning_rate):
        super(PolicyValueNet, self).__init__()
        self.conv_seq = nn.Sequential()
        input_planes = 1
        for i,conv_item in enumerate(conv_filters):
            self.conv_seq.add_module(f'conv{conv_item}_{i}',conv3x3(input_planes,conv_item))
            self.conv_seq.add_module(f'bn{conv_item}_{i}',bn2d(conv_item))
            self.conv_seq.add_module(f'relu{conv_item}_{i}',nn.ReLU())
            input_planes = conv_item

        self.resnet_seq = nn.Sequential()
        for i,resnet_item in enumerate(resnet_filters):
            self.resnet_seq.add_module(f'resnet{resnet_item}_{i}',ResnetBlock(input_planes,resnet_item))
            input_planes = resnet_item
        input_intermidate = input_planes
        #概率层
        self.policy_seq = nn.Sequential()
        for i,policy_item in enumerate(policy_filters):
            self.policy_seq.add_module(f'policy{policy_item}_{i}',conv3x3(input_planes,policy_item))
            self.conv_seq.add_module(f'bn{policy_item}_{i}', bn2d(policy_item))
            self.conv_seq.add_module(f'relu{policy_item}_{i}', nn.ReLU())
            input_planes = policy_item
        self.policy_seq.add_module('policy_flatten',nn.Flatten())
        self.policy_seq.add_module('policy_softmax', nn.Softmax())

        #价值层
        self.value_seq = nn.Sequential()
        self.value_seq.add_module('value_conv2d',nn.Conv2d(input_intermidate,3,3,padding=3))
        self.value_seq.add_module('value_Bn', bn2d(3))
        self.value_seq.add_module('value_relu',nn.ReLU())
        self.value_seq.add_module('value_flatten',nn.Flatten())



    def forward(self,x):
        out = self.conv_seq(x)
        out = self.resnet_seq(out)
        policy_out = self.policy_seq(out)
        policy_out = nn.functional.linear(policy_out.size(),cfg.MAX_LEN**2)
        value_out = self.value_seq(out)
        value_out = nn.functional.linear(value_out.size(),1)

        return policy_out,value_out



