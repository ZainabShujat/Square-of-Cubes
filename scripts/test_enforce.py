from core.levels import enforce_min_sizes
inv = {4:9}
print('before', inv, 'area', sum(k*k*v for k,v in inv.items()))
enf = enforce_min_sizes(inv, 4, 12*12)
print('after', enf, 'area', sum(k*k*v for k,v in enf.items()))
