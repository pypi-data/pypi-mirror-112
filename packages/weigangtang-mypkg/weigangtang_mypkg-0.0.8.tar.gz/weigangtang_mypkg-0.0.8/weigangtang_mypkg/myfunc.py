# require minimal python packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib
import sys, time, subprocess
import re

def find_number_from_string(string, maxlen=10):
    pattern = '[0-9]{1,%d}' % maxlen
    number_list = re.findall(pattern, string)
    number_list = [int(item) for item in number_list]
    return number_list

def save_list(alist, path):
    pd.DataFrame(index=alist).to_csv(path, header=None)

def load_list(path):
    return pd.read_csv(path, index_col=0, header=None).index.tolist()

def get_ticks(xmin, xmax, incr, mode='outer'):
    
    if mode == 'outer':
        sint = np.floor(xmin / incr)
        eint = np.ceil(xmax / incr)
    
    if mode == 'inner':
        sint = np.ceil(xmin / incr)
        eint = np.floor(xmax / incr)
    
    ticks = np.arange(sint, eint+1) * incr
    return ticks

def union(*args):
    output = set(args[0])
    for item in args[1:]: output = output.union(item)
    return np.sort(list(output)).tolist()

def intersection(*args):
    output = set(args[0])
    for item in args[1:]: output = output.intersection(item)
    return np.sort(list(output)).tolist()

def difference(alist, blist):
    set_union = set(alist).union(blist)
    set_inter = set(alist).intersection(blist)
    return list(set_union.difference(set_inter))

def sort_by_list(alist, blist):
    # elements in alist were sorted according to the order of blist
    # elements in alist but not in blist will be ignored
    alist_sorted = [item for item in blist if item in alist]
    if len(alist_sorted) < len(alist): 
        print('{:d} items were ignored.'.format(len(alist)-len(alist_sorted))) 
        print(list(set(alist).difference(alist_sorted)))
    return alist_sorted

def find_duplicates(alist):
    alist = list(alist)
    index_dup = [i for i, x in enumerate(alist) if alist.count(x) > 1]
    return index_dup

# def find_duplicate(alist):
#   nondup, dup = [], []
#   for item in alist:
#       if item not in nondup: nondup.append(item)
#       else:dup.append(item)
#   dup = np.unique(dup).tolist()
#   return dup

def find_major(x):
    uqval, count  = np.unique(x, return_counts=True)
    return uqval[np.argmax(count)]

def count_major(x):
    mjr = find_major(x)
    return sum(x == mjr)

# Usually, pts and pts_ref should be 2d array
# Special Cases:
#     - pts is a scalar, pts_ref is a list or 1d array
#     - pts is a list or 1d array, pts_ref is a list or 1d array
#     - pts is a list or 1d array, pts_ref is 2d array
def find_nn_index(pts, pts_ref, n=1):
    
    pts = np.array(pts)
    pts_ref = np.array(pts_ref)
    
    if (pts.ndim == 0) & (pts_ref.ndim == 1):
        pts = pts[np.newaxis, np.newaxis]
        pts_ref = pts_ref[:, np.newaxis]
        
    elif (pts.ndim == 1) & (pts_ref.ndim == 1):
        pts = pts[:, np.newaxis]
        pts_ref = pts_ref[:, np.newaxis]
    
    elif (pts.ndim == 1) & (pts_ref.ndim == 2):
        pts = pts[np.newaxis, :]
    
    assert pts_ref.ndim == 2
    assert pts.shape[1] == pts_ref.shape[1]
        
    n1 = pts.shape[0]
    n2 = pts_ref.shape[0]

    tensor1 = np.repeat(pts[:, :, np.newaxis], n2, axis=2)
    tensor1 = tensor1.transpose([0, 2, 1])

    tensor2 = np.repeat(pts_ref[:, :, np.newaxis], n1, axis=2)
    tensor2 = tensor2.transpose([2, 0, 1])

    dist = np.sum(np.abs(tensor1 - tensor2), axis=2)
    nn_indx = np.argsort(dist, axis=1)

    nn_indx = nn_indx[:, :n].squeeze()
    return nn_indx

# def find_nn_index(pt, pts, n=1):
#     assert len(pts.shape) == 2
#     assert len(pt) == pts.shape[1]

#     dist = np.sum(np.abs(pts - pt), axis=1)

#     nn_indx = np.argsort(dist)[:n]
#     return nn_indx

# recursive function
def melt_list(*in_list):
    in_list = list(in_list)
    out_list = []
    if len(in_list) > 2:
        alist = in_list.pop(0)
        for a in alist:
            out_list += [[a] + b for b in melt_list(*in_list)]
    else:
        alist, blist = in_list
        for a in alist:
            out_list += [[a] + [b] for b in blist]
    return out_list


def countna(x, axis=None):
	return np.sum(np.isnan(x), axis=axis)


# Color Tools -----------------------------------------------------

# rgb must be a list or tuple, such as [100, 120, 80]
# values must be between 0 and 255
def rgb_to_hex(rgb):
	return '#%02x%02x%02x' % tuple(rgb)

# get_cmap_hex('Set2')
def get_cmap_hex(name):
    cmap = plt.cm.get_cmap(name)
    colors = []
    for i in range(cmap.N):
        rgba = cmap(i)
        chex = matplotlib.colors.rgb2hex(rgba)
        colors.append(chex)
    return colors

def get_cmap_hex_cgrad(name, n, start=0, end=1):
    colors = np.array(get_cmap_hex(name))
    ncolor = len(colors)

    sidx = np.round(start * ncolor).astype(int)
    eidx = np.round(end * ncolor).astype(int) - 1
    sel_idx = np.round(np.linspace(sidx, eidx, n)).astype(int)

    sel_colors = colors[sel_idx]
    return sel_colors

def plot_cmap_colors(cmap_name):
    cmap = plt.cm.get_cmap(cmap_name)
    n = cmap.N
    x, y = range(n), [0]*n

    fig, ax = plt.subplots()
    ax.scatter(x, y, c=cmap.colors, s=200)
    ax.set_xticks(x)
    fig.set_size_inches([12, 2])

# -----------------------------------------------------------------

def digitize(value, bins):

	if np.isscalar(value): value = np.array([value])

	value = np.array(value)
	value_d = value.copy() * np.nan

	bins = np.sort(bins); n_bin = len(bins)

	value_d[value <= bins[0]] = 0
	for i in range(n_bin):
		value_d[value > bins[i]] = i + 1

	if len(value_d) == 1: value_d = value_d[0]
	return value_d

def movfunc(tensor, k, axis=-1, gfunc=np.mean):
    dims = list(tensor.shape)
    slcs = [slice(0, i) for i in dims]

    n =  dims[axis] - k + 1 # new dim for axis of moving window

    tensor_list = [] 
    for i in range(k):
        slcs[axis] = slice(i, i+n)
        tensor_list.append(tensor[tuple(slcs)]) # using tuple avoid warning message

    tensor_sm = gfunc(np.stack(tensor_list), axis=0)
    return tensor_sm

# find valid index for a list of arrary
def find_vidx(*args):

    n = len(args[0])
    assert all([len(item)==n for item in args]) # length of arrays must be equal

    vidx = np.ones(n).astype(bool) # valid index
    for item in args:
    	vidx = vidx & ~np.isnan(item) & ~np.isinf(item)
    return vidx


def countdown_timer(hour=0, minute=0, second=0, text_frame='Time Elapsed: {}'):

    tot_sec = hour * 3600 + minute * 60 + second
    tot_sec = int(tot_sec)

    text_frame = text_frame.replace('{}', '{:02d}:{:02d}:{:02d}')

    for rem in range(0, tot_sec)[::-1]:

        rem_h, rem_m, rem_s = rem // 3600, (rem % 3600) // 60, rem % 60

        sys.stdout.write('\r')
        sys.stdout.write(text_frame.format(rem_h, rem_m, rem_s))
        sys.stdout.flush()

        time.sleep(1)

def is_equal_array(a, b):
    a[np.isnan(a)] = 999
    b[np.isnan(b)] = 999
    return np.sum(np.abs(a - b)) == 0
