import csv,ast

pa="/home/me/final/media/media/"+"PR5001"+"/m.csv"
 
with open(pa,'r') as f:
	w=csv.DictReader(f)
	for r in w:
		m=dict(r)
f.close()

z={}
for k,v in m.items():
	if int(k) <= 5 and int(k) >= 16:
		z[int(k)]=str(v)
		z[int(k)]=ast.literal_eval(v)
	elif int(k) >= 9 :
		v=v[0:9]+" 0 ,"+v[33:]
		z[int(k)]=ast.literal_eval(v)
	else:
		v=v[0:9]+" 0 ,"+v[32:]
		z[int(k)]=ast.literal_eval(v)

