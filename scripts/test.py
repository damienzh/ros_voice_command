import os

model_name = 'zh-cn'
p = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
base_path = os.path.join(p, 'param', model_name)
hmm_path = os.path.join(base_path, model_name + '.cd_cont_5000')
lm_file = os.path.join(base_path, model_name + '.lm.bin')
dic_file = os.path.join(base_path, model_name + '.dic')

print hmm_path
print dic_file
print lm_file