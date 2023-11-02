from generating_archs import *
from settings import *
from icecream import ic


catalan_codes = catalan(cnt, ind, arches, init)

result = list(map(catal_into_arch_indx, catalan_codes))
result = list(map(making_arches, result))
result = [item for item in result if item is not None]
result = list(map(block, result))
result = remove_repeated(result)

save_codes(result, in_path)
