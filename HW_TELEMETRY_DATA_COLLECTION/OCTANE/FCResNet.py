import torch
import torch.nn as nn
import torch.nn.functional as F
d = 50

class FCResBlock(nn.Module):
    def __init__(self, in_features, out_features):
        super(FCResBlock, self).__init__()
        self.fc1 = nn.Linear(in_features, out_features)
        self.fc2 = nn.Linear(out_features, out_features)
        # Use a linear layer to match dimensions if necessary; otherwise, Identity.
        self.shortcut = nn.Linear(in_features, out_features) if in_features != out_features else nn.Identity()
    
    def forward(self, x):
        residual = self.shortcut(x)
        out = F.relu(self.fc1(x))
        out = self.fc2(out)
        out += residual
        return F.relu(out)

class TabularResNet(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(TabularResNet, self).__init__()
        # Initial transformation
        self.fc_in = nn.Linear(input_dim, 64)
        # Stacking residual blocks
        self.block1 = FCResBlock(64, 128)
        self.block2 = FCResBlock(128, 128)
        self.block3 = FCResBlock(128, 128)
        self.block4 = FCResBlock(128, 128)
        self.block5 = FCResBlock(128, 128)
        self.block6 = FCResBlock(128, 128)
        self.block7 = FCResBlock(128, 128)
        self.block8 = FCResBlock(128, 128)
        self.block9 = FCResBlock(128, 128)
        self.block10 = FCResBlock(128, 128)
        self.block11 = FCResBlock(128, 128)
        self.block12 = FCResBlock(128, 128)
        self.block13 = FCResBlock(128, 128)
        self.block14 = FCResBlock(128, 128)
        self.block15 = FCResBlock(128, 128)
        self.block16 = FCResBlock(128, 128)
        self.block17 = FCResBlock(128, 128)
        self.block18 = FCResBlock(128, 64)
        # Final output layer
        self.fc_out = nn.Linear(64, output_dim)
    
    def forward(self, x):
        x = F.relu(self.fc_in(x))
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        x = self.block4(x)
        x = self.block5(x)
        x = self.block6(x)
        x = self.block7(x)
        x = self.block8(x)
        x = self.block9(x)
        x = self.block10(x)
        x = self.block11(x)
        x = self.block12(x)
        x = self.block13(x)
        x = self.block14(x)
        x = self.block15(x)
        x = self.block16(x)
        x = self.block17(x)
        x = self.block18(x)
        return self.fc_out(x)

