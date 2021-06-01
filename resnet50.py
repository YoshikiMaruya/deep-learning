import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optimizers
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import torchvision
import torchvision.transforms as transforms
from sklearn.metrics import accuracy_score
from torchvision.datasets import FashionMNIST
from google import colab
colab.drive.mount('/content/gdrive')

class ResNet50(nn.Module):
    def __init__(self, output_dim):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 64,
                               kernel_size=(7, 7),
                               stride=(2, 2),
                               padding=3)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=(3, 3),
                                  stride=(2, 2),
                                  padding=1)
        # Block 1
        self.block0 = self._building_block(256, channel_in=64)
        self.block1 = nn.ModuleList([
            self._building_block(256) for _ in range(2)
        ])
        self.conv2 = nn.Conv2d(256, 512,
                               kernel_size=(1, 1),
                               stride=(2, 2))
        # Block 2
        self.block2 = nn.ModuleList([
            self._building_block(512) for _ in range(4)
        ])
        self.conv3 = nn.Conv2d(512, 1024,
                               kernel_size=(1, 1),
                               stride=(2, 2))
        # Block 3
        self.block3 = nn.ModuleList([
            self._building_block(1024) for _ in range(6)
        ])
        self.conv4 = nn.Conv2d(1024, 2048,
                               kernel_size=(1, 1),
                               stride=(2, 2))
        # Block 4
        self.block4 = nn.ModuleList([
            self._building_block(2048) for _ in range(3)
        ])
        self.avg_pool = GlobalAvgPool2d()  # TODO: GlobalAvgPool2d
        self.fc = nn.Linear(2048, 1000)
        self.out = nn.Linear(1000, output_dim)
    def forward(self, x):
        h = self.conv1(x)
        h = self.bn1(h)
        h = self.relu1(h)
        h = self.pool1(h)
        h = self.block0(h)
        for block in self.block1:
            h = block(h)
        h = self.conv2(h)
        for block in self.block2:
            h = block(h)
        h = self.conv3(h)
        for block in self.block3:
            h = block(h)
        h = self.conv4(h)
        for block in self.block4:
            h = block(h)
        h = self.avg_pool(h)
        h = self.fc(h)
        h = torch.relu(h)
        h = self.out(h)
        y = torch.log_softmax(h, dim=-1)
        return y
    def _building_block(self,
                        channel_out,
                        channel_in=None):
        if channel_in is None:
            channel_in = channel_out
        return Block(channel_in, channel_out)

class Block(nn.Module):
  def __init__(self, channel_in, channel_out):
      super().__init__()
      channel = channel_out // 4
      # 1x1 の畳み込み
      self.conv1 = nn.Conv2d(channel_in, channel,
                             kernel_size=(1, 1))
      self.bn1 = nn.BatchNorm2d(channel)
      self.relu1 = nn.ReLU()
      # 3x3 の畳み込み
      self.conv2 = nn.Conv2d(channel, channel,
                             kernel_size=(3, 3),
                             padding=1)
      self.bn2 = nn.BatchNorm2d(channel)
      self.relu2 = nn.ReLU()
      # 1x1 の畳み込み
      self.conv3 = nn.Conv2d(channel, channel_out,
                             kernel_size=(1, 1),
                             padding=0)
      self.bn3 = nn.BatchNorm2d(channel_out)
      # skip connection用のチャネル数調整
      self.shortcut = self._shortcut(channel_in, channel_out)

      self.relu3 = nn.ReLU()
  def forward(self, x):
      h = self.conv1(x)
      h = self.bn1(h)
      h = self.relu1(h)
      h = self.conv2(h)
      h = self.bn2(h)
      h = self.relu2(h)
      h = self.conv3(h)
      h = self.bn3(h)
      shortcut = self.shortcut(x)
      y = self.relu3(h + shortcut)  # skip connection
      return y
  def _shortcut(self, channel_in, channel_out):
      if channel_in != channel_out:
          return self._projection(channel_in, channel_out)
      else:
          return lambda x: x
  def _projection(self, channel_in, channel_out):
      return nn.Conv2d(channel_in, channel_out,
                       kernel_size=(1, 1),
                       padding=0)

class GlobalAvgPool2d(nn.Module):
  def __init__(self,
               device='cpu'):
      super().__init__()
  def forward(self, x):
      return F.avg_pool2d(x, kernel_size=x.size()[2:]).view(-1, x.size(1))

if __name__ == '__main__':
    np.random.seed(1234)
    torch.manual_seed(1234)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    '''
    データの読み込み
    '''

    d_dir='gdrive/MyDrive/ProjectExperiment/Datasets/'

    #そのままだとPIL（Python Imaging Library）の画像形式でDatasetを
    #を作ってしまうのでtransforms.toTensorでTensorに変換
    fashion_mnist_train=FashionMNIST(d_dir,train=True, download=True,transform=transforms.ToTensor())
    fashion_mnist_test=FashionMNIST(d_dir,train=False, download=True,transform=transforms.ToTensor())

    #バッチサイズが128のDataLoaderを作成
    #データローダーはミニバッチを作成するため
    batch_size=128
    train_dataloader=DataLoader(fashion_mnist_train,batch_size=batch_size,shuffle=True)
    test_dataloader=DataLoader(fashion_mnist_test,batch_size=batch_size,shuffle=False)

    # モデルの構築

    model = ResNet50(10).to(device)

    # モデルの学習・評価

    def compute_loss(label, pred):
        return criterion(pred, label)
    def train_step(x, t):
        model.train()
        preds = model(x)
        loss = compute_loss(t, preds)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        return loss, preds
    def test_step(x, t):
        model.eval()
        preds = model(x)
        loss = compute_loss(t, preds)
        return loss, preds
    criterion = nn.NLLLoss()
    optimizer = optimizers.Adam(model.parameters(), weight_decay=0.01)
    epochs = 5
    for epoch in range(epochs):
        train_loss = 0.
        test_loss = 0.
        test_acc = 0.
        for (x, t) in train_dataloader:
            x, t = x.to(device), t.to(device)
            loss, _ = train_step(x, t)
            train_loss += loss.item()
        train_loss /= len(train_dataloader)
        for (x, t) in test_dataloader:
            x, t = x.to(device), t.to(device)
            loss, preds = test_step(x, t)
            test_loss += loss.item()
            test_acc += \
                accuracy_score(t.tolist(), preds.argmax(dim=-1).tolist())
        test_loss /= len(test_dataloader)
        test_acc /= len(test_dataloader)
        print('Epoch: {}, Valid Cost: {:.3f}, Valid Acc: {:.3f}'.format(
            epoch+1,
            test_loss,
            test_acc
        ))
