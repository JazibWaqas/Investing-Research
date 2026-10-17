import sys; sys.path.insert(0,'scripts')
from cf import get
u,o=sys.argv[1:3]
r=get(u); open(o,'wb').write(r.content); print(r.status_code,len(r.content))
