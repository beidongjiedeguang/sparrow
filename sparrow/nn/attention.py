import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

import einops
from einops import rearrange, reduce, asnumpy, parse_shape
from einops.layers.torch import Rearrange, Reduce
from torch import einsum


def check_shape(tensor, pattern, **kwargs):
    return einops.rearrange(tensor, f"{pattern} -> {pattern}", **kwargs)


class ScaledDotProductAttention(nn.Module):
    def __init__(self, d_out, d_k, d_v, h, dropout=0.1):
        """
        :param d_out: output dimension
        :param d_k: dimension of key
        :param d_v: dimension of value
        :param h: number of heads
        :param dropout: dropout rate
        """
        super(ScaledDotProductAttention, self).__init__()
        self.d_out = d_out
        self.d_k = d_k
        self.d_v = d_v
        self.h = h
        self.dropout = nn.Dropout(dropout)

        self.fc_q = nn.Linear(d_out, h * d_k)
        self.fc_k = nn.Linear(d_out, h * d_k)
        self.fc_v = nn.Linear(d_out, h * d_v)
        self.fc_o = nn.Linear(h * d_v, d_out)

        self.init_weights()

    def init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0.0)
            elif isinstance(m, nn.LayerNorm):
                nn.init.constant_(m.weight, 1.0)
                nn.init.constant_(m.bias, 0.0)
            elif isinstance(m, nn.Dropout):
                nn.init.constant_(m.weight, 1.0)
                nn.init.constant_(m.bias, 0.0)
            elif isinstance(m, nn.Conv2d):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0.0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out')
                nn.init.constant_(m.bias, 0.0)

    def forward(self, queries, keys, values, mask=None, weights=None):
        """
        :param queries: (batch_size, nq, d_out)
        :param keys: (batch_size, nk, d_out)
        :param values: (batch_size, nk, d_out)
        :param mask: (batch_size, h, nq, nk)
        :param weights: (batch_size, h, nq, nk)
        """
        bs, nq = queries.shape[:2]
        nk = keys.shape[1]

        q = self.fc_q(queries)


def attention_origin(q, k, v):
    """
    attention(q, k, v) = softmax( (q  k.T) / sqrt(dk) )  v
    """
    # for pytorch
    s = q.shape[-1] ** -0.5
    return (q @ k.t() * s).softmax(dim=-1) @ v


def attention(K, V, Q):
    _, n_channels, _ = K.shape
    A = torch.einsum('bct,bcl->btl', [K, Q])
    A = F.softmax(A * n_channels ** (-0.5), 1)
    R = torch.einsum('bct,btl->bcl', [V, A])
    return torch.cat((R, Q), dim=1)


class MultiHeadAttentionNew(nn.Module):
    def __init__(self, n_head, d_model, d_k, d_v, dropout=0.1):
        super().__init__()
        self.n_head = n_head

        self.w_qs = nn.Linear(d_model, n_head * d_k)
        self.w_ks = nn.Linear(d_model, n_head * d_k)
        self.w_vs = nn.Linear(d_model, n_head * d_v)

        nn.init.normal_(self.w_qs.weight, mean=0, std=np.sqrt(2.0 / (d_model + d_k)))
        nn.init.normal_(self.w_ks.weight, mean=0, std=np.sqrt(2.0 / (d_model + d_k)))
        nn.init.normal_(self.w_vs.weight, mean=0, std=np.sqrt(2.0 / (d_model + d_v)))

        self.fc = nn.Linear(n_head * d_v, d_model)
        nn.init.xavier_normal_(self.fc.weight)
        self.dropout = nn.Dropout(p=dropout)
        self.layer_norm = nn.LayerNorm(d_model)

    def forward(self, q, k, v, mask=None):
        residual = q
        q = rearrange(self.w_qs(q), 'b l (head k) -> head b l k', head=self.n_head)
        k = rearrange(self.w_ks(k), 'b t (head k) -> head b t k', head=self.n_head)
        v = rearrange(self.w_vs(v), 'b t (head v) -> head b t v', head=self.n_head)
        attn = torch.einsum('hblk,hbtk->hblt', [q, k]) / np.sqrt(q.shape[-1])
        if mask is not None:
            attn = attn.masked_fill(mask[None], -np.inf)
        attn = torch.softmax(attn, dim=3)
        output = torch.einsum('hblt,hbtv->hblv', [attn, v])
        output = rearrange(output, 'head b l v -> b l (head v)')
        output = self.dropout(self.fc(output))
        output = self.layer_norm(output + residual)
        return output, attn


class Self_Attn_GAN(nn.Module):
    """ Self attention Layer"""

    def __init__(self, in_dim):
        super().__init__()
        self.query_conv = nn.Conv2d(in_dim, out_channels=in_dim // 8, kernel_size=1)
        self.key_conv = nn.Conv2d(in_dim, out_channels=in_dim // 8, kernel_size=1)
        self.value_conv = nn.Conv2d(in_dim, out_channels=in_dim, kernel_size=1)
        self.gamma = nn.Parameter(torch.zeros([1]))

    def forward(self, x):
        proj_query = rearrange(self.query_conv(x), 'b c h w -> b (h w) c')
        proj_key = rearrange(self.key_conv(x), 'b c h w -> b c (h w)')
        proj_value = rearrange(self.value_conv(x), 'b c h w -> b (h w) c')
        energy = torch.bmm(proj_query, proj_key)
        attention = F.softmax(energy, dim=2)
        out = torch.bmm(attention, proj_value)
        out = x + self.gamma * rearrange(out, 'b (h w) c -> b c h w',
                                         **parse_shape(x, 'b c h w'))
        return out, attention


class KroneckerSelfAttention(nn.Module):
    def __init__(self, dim, heads, dim_heads=32):
        super().__init__()
        hidden_dim = heads * dim_heads

        self.heads = heads
        self.to_qkv = nn.Conv1d(dim, hidden_dim * 3, 1, bias=False)
        self.to_out = nn.Conv1d(hidden_dim, dim, 1)

    def forward(self, x):
        h = x.shape[-2]

        x = torch.cat((x.mean(dim=-1), x.mean(dim=-2)), dim=-1)

        qkv = self.to_qkv(x)
        q, k, v = rearrange(qkv, 'b (qkv h d) n -> qkv b h d n', h=self.heads, qkv=3)

        dots = einsum('bhdi,bhdj->bhij', q, k)
        attn = dots.softmax(dim=-1)
        out = einsum('bhij,bhdj->bhdi', attn, v)

        out = rearrange(out, 'b h d n -> b (h d) n')
        out = self.to_out(out)

        # outer sum
        out = rearrange(out[..., :h], 'b c (n 1) -> b c n 1') + rearrange(out[..., h:], 'b c (1 n) -> b c 1 n')
        return out
