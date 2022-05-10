# from einops import rearrange, reduce
import einops


def repeat(tensor, n, axis=-1):
    shape = tensor.shape
    dims = len(shape)
    if dims == 1:
        if axis == 0:
            res = einops.repeat(tensor, "w -> h w", h=n)
        else:
            res = einops.repeat(tensor, "h -> h w", w=n)
    elif dims == 2:
        if axis == 0:
            res = einops.repeat(tensor, "h w -> c h w", c=n)
        else:
            res = einops.repeat(tensor, "h w -> h w c", c=n)
    elif dims == 3:
        if axis == 0:
            res = einops.repeat(tensor, "h w c -> b h w c", b=n)
        elif axis == 1:
            res = einops.repeat(tensor, "h w c -> h b w c", b=n)
        else:
            res = einops.repeat(tensor, "h w c -> h w c b", b=n)
    else:
        raise ValueError
    return res
