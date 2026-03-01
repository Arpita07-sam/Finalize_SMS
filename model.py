import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F

class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        
        self.base_model = models.resnet18(pretrained=True)
        self.base_model.conv1 = nn.Conv2d(
            1, 64, kernel_size=7, stride=2, padding=3, bias=False
        )

        num_features = self.base_model.fc.in_features
        self.base_model.fc = nn.Linear(num_features, 256)

    # def forward_once(self, x):
    #     return self.base_model(x)
    
    def forward_once(self, x):
        x = self.base_model(x)
        return F.normalize(x, p=2, dim=1)

    def forward(self, anchor, positive, negative):
        anchor_out = self.forward_once(anchor)
        positive_out = self.forward_once(positive)
        negative_out = self.forward_once(negative)
        return anchor_out, positive_out, negative_out
    
 

    