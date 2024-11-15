import torch


def dot_product(emb1, emb2):
    return torch.dot(emb1, emb2).item()
