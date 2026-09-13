from pathlib import Path
import sys,json,math,hashlib,re
P=Path(__file__).resolve().parent.parent;W=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'auxiliar-optimizacion-v76/libs'))
exec((P/'auxiliar-optimizacion-v76/estudio.py').read_text().split('out=[]')[0])
W=P/'auxiliar-b2-v77'
from shapely.affinity import rotate,translate
# All auxiliary coordinates u=-Y, v=X; elevation is absolute survey datum.
shaft=box(11.05,-5.05,14.35,1.55);wait=box(11.3,1.55,14.1,6.95)
N=box(15.9,2,21.7,7.6);V=box(20.85,-12.9,26.55,-7.3);S=box(15.1,-19.0,20.7,-13.2)
cn=np.array([13.0,5.05]);tend=math.radians(80)
cl=np.array([12.7+4.5*(1-math.cos(tend))+1.5*math.sin(tend),-5.45-4.5*math.sin(tend)-1.5*math.cos(tend)]);R=2.9
dn=Point(cn).buffer(R,96);dl=Point(cl).buffer(R,96)
upper=unary_union([dn,box(11.05,1.55,14.35,3.0),box(15.0,2.25,15.9,7.35)]).difference(shaft)
def car_at(u,v,theta):
 # Vehicle 5.00 x 2.10; theta is heading from +u, centre reference.
 return translate(rotate(box(-2.5,-1.05,2.5,1.05),math.degrees(theta),origin=(0,0)),u,v)
def sweep(poses):return unary_union([car_at(*p) for p in poses])
# Rear axle R=4.5 m quarter turn: axle initially south-facing below shaft portal.
poses=[]
for vv in np.linspace(-1.0,-5.45,45):poses.append((12.7,vv-1.5,-math.pi/2))
for t in np.linspace(0,tend,100):
 rear=np.array([12.7+4.5*(1-math.cos(t)),-5.45-4.5*math.sin(t)])
 heading=-math.pi/2+t;centre=rear+1.5*np.array([math.cos(heading),math.sin(heading)])
 poses.append((*centre,heading))
# Stop at 80 degrees on the turntable. The platform completes the remaining rotation.
sw=sweep(poses);lowerlink=sw.buffer(.20,join_style=1).difference(shaft)
lowerG=unary_union([dl,lowerlink,box(20.0,-12.65,20.85,-7.55),box(15.35,-13.2,20.45,-12.1)])
lowerT=unary_union([box(14.8,-13.2,20.85,-7.20),lowerlink]).difference(unary_union([V,S]))
# Reorient/park from turntable: circular centre paths with final heading along the bay.
def arc_to(start,end,heading):
 # Local +x is final heading; initial heading is chosen by the turntable.
 cs,sn=math.cos(heading),math.sin(heading);M=np.array([[cs,-sn],[sn,cs]])
 end=np.array(end);q=M.T@(np.array(start)-end);dx,dy=q
 if abs(dy)<1e-6:return [(float(a[0]),float(a[1]),heading) for a in np.linspace(start,end,80)]
 ry=(dx*dx+dy*dy)/(2*dy);centre=np.array([0,ry]);r=abs(ry)
 a0=math.atan2(q[1]-ry,q[0]);a1=math.atan2(-ry,0);da=(a1-a0+math.pi)%(2*math.pi)-math.pi
 result=[]
 for a in np.linspace(a0,a0+da,100):
  pos=centre+r*np.array([math.cos(a),math.sin(a)]);tangent=a+(math.pi/2 if da>0 else -math.pi/2)
  pp=end+M@pos;result.append((*pp,tangent+heading))
 return result
park_paths={}
for home,p,ctr,heading in [('Norte',N,cn,0),('Villa',V,cl,0),('Sur',S,cl,-math.pi/2)]:
 x0,y0,x1,y1=p.bounds
 ends=[((x0+x1)/2,y0+1.4),((x0+x1)/2,y0+4.2)] if heading==0 else [(x0+1.4,(y0+y1)/2),(x0+4.2,(y0+y1)/2)]
 park_paths[home]=[arc_to(ctr,q,heading) for q in ends]
 # Reserve actual swept surface at each portal, with a 0.1m tolerance; keep private rooms intact.
 swept=unary_union([sweep(z) for z in park_paths[home]]).buffer(.1)
 if home=='Norte':upper=unary_union([upper,swept.difference(N)]).difference(shaft)
 else:lowerG=unary_union([lowerG,swept.difference(unary_union([V,S]))]).difference(shaft)
configs=[
 {'id':'B2-1','name':'Dos giros separados · tres paradas','levels':[{'z':16.51,'rooms':[('Norte',N)],'man':upper,'tables':[cn]},{'z':14.56,'rooms':[('Villa',V),('Sur',S)],'man':lowerG,'tables':[cl]}]},
 {'id':'B2-2','name':'Giro superior · distribuidor inferior en T','levels':[{'z':16.51,'rooms':[('Norte',N)],'man':upper,'tables':[cn]},{'z':14.56,'rooms':[('Villa',V),('Sur',S)],'man':lowerT,'tables':[]}]}
]
# Projected construction is an indicative 0.25m perimeter allowance, not structural design.
for cfg in configs:
 for lev in cfg['levels']:
  lev['foot']=unary_union([shaft,lev['man'],*[p for _,p in lev['rooms']]]).buffer(.25,join_style=2)
  lev['man']=lev['man'].difference(shaft)
 # Reserve separate structural envelopes at the two stops; only the shaft is shared.
 cfg['levels'][0]['foot']=cfg['levels'][0]['foot'].difference(cfg['levels'][1]['foot'].difference(shaft.buffer(.25)))
def door(ax,p,home):
 x0,y0,x1,y1=p.bounds
 if home=='Sur':xx=[x0+.25,x1-.25];yy=[y1,y1]
 else:xx=[x0,x0];yy=[y0+.25,y1-.25]
 ax.plot(xx,yy,c='white',lw=4);ax.plot(xx,yy,c='#315d50',lw=.8,ls='--')
def context(ax):
 paint(ax,pa,'#f4f2e9');paint(ax,strip,'#ecd397',alpha=.8);paint(ax,alignment,'none',ec='#b47d29',lw=1.6);paint(ax,villa,'#d8dcda')
 for h in houses:paint(ax,h,'#dfe3dd',hatch='//')
 paint(ax,shaft,'#517e9f');paint(ax,wait,'#edc96b');ax.annotate('Espera en superficie\n2,80 × 5,40',xy=(12.7,6.95),xytext=(8.3,9.5),ha='center',fontsize=6,arrowprops=dict(arrowstyle='-',color='#9f7d39'),bbox=dict(fc='#fff6db',ec='none',alpha=.9))
 ax.text(12.7,-1.75,'LIFT\n3,30 × 6,60',ha='center',va='center',fontsize=6,color='white');ax.text(3,0,'VILLA MANUELA',ha='center',fontsize=7)
 ax.set(xlim=(0,29),ylim=(-21,11),xlabel='Este · u = −Y (m)',ylabel='Norte · X (m)');ax.set_aspect('equal');ax.grid(alpha=.14)
 ax.annotate('N',xy=(27.5,10),xytext=(27.5,7),ha='center',arrowprops=dict(arrowstyle='->'))
diagnostics=[]
for cfg in configs:
 fig,axs=plt.subplots(1,2,figsize=(15,9))
 for ax,lev in zip(axs,cfg['levels']):
  context(ax);paint(ax,lev['man'],'#dfd19f',alpha=.95)
  for home,p in lev['rooms']:
   paint(ax,p,'#92c2ae',ec='#315d50',alpha=.93,lw=1.3);door(ax,p,home)
   for path in park_paths[home]:paint(ax,car_at(*path[-1]),'#fbfaf3')
   x,y=p.centroid.coords[0];ax.text(x,y,f'{home}\n{p.area:.2f} m²',ha='center',va='center',fontsize=7,bbox=dict(fc='white',ec='none',alpha=.9))
  for t in lev['tables']:
   paint(ax,Point(t).buffer(2.9),'none',ec='#896326',lw=1.6);paint(ax,Point(t).buffer(2.5),'none',ec='#896326',lw=.7);ax.text(*t,'GIRO\nØ libre 5,80',ha='center',va='center',fontsize=6)
  # Visible relation to opposite level: cannot stack at only 1.95m apart.
  other=cfg['levels'][1] if lev is cfg['levels'][0] else cfg['levels'][0]
  conflict=lev['foot'].intersection(other['foot']).difference(shaft.buffer(.25));paint(ax,conflict,'#d95d55',alpha=.9)
  if lev['z']==14.56:
   pts=np.array(poses);ax.plot(pts[:,0],pts[:,1],c='#95612f',ls='--',lw=1);ax.text(1,-20,'Trazo: aproximación SUV de prueba\n80° conduciendo; giro final mediante plataforma',fontsize=7)
  ax.set_title(f"{cfg['id']} · {lev['z']:.2f} m\n{cfg['name']}",fontsize=12)
 fig.tight_layout();fig.savefig(P/f'ESTUDIO_B2-v77-{cfg["id"]}.png',dpi=140);plt.close(fig)
 foot=unary_union([l['foot'] for l in cfg['levels']]);vol=inc=missing=exposed=0;dep=[];covers=[];step=.25
 u0,v0,u1,v1=foot.bounds
 for u in np.arange(u0+.125,u1,.25):
  for v in np.arange(v0+.125,v1,.25):
   pt=Point(u,v)
   if not foot.covers(pt):continue
   z=height(u,v)
   if z is None:missing+=.0625;continue
   active=[l for l in cfg['levels'] if l['foot'].covers(pt)];floor=min(l['z'] for l in active);bottom=floor-.25
   if shaft.covers(pt):bottom=14.56-.6
   vol+=max(0,z-bottom)*.0625;dep.append(z-bottom)
   existing=z
   for h,hs in zip(houses,[16.51,14.56]):
    if h.covers(pt):existing=min(existing,hs-.25)
   inc+=max(0,existing-bottom)*.0625
   top=max(l['z']+2.55 for l in active)
   if not shaft.buffer(.26).covers(pt) and not any(h.covers(pt) for h in houses):
    covers.append(z-top)
    if z<top:exposed+=.0625
 hits=[]
 for lev in cfg['levels']:
  # Floor at SS level is compatible; other level crossing the SS slab is not.
  for label,h,ssfloor in [('norte',houses[0],16.51),('sur',houses[1],14.56)]:
   if lev['z']+.05<ssfloor<lev['z']+2.55:hits.append({'level':lev['z'],'building':label,'slab_conflict_m2':lev['foot'].intersection(h).area})
 maneuver=sum(l['man'].area for l in cfg['levels'])
 dct={'id':cfg['id'],'name':cfg['name'],'footprint_m2':foot.area,'sum_levels_m2':sum(l['foot'].area for l in cfg['levels']),'private_garages_m2':sum(p.area for l in cfg['levels'] for _,p in l['rooms']),'maneuver_m2':maneuver,'excavation_m3':vol,'additional_excavation_m3':inc,'surface_sample_missing_m2':missing,'depth_range_m':[min(dep),max(dep)],'roof_exposed_outside_houses_m2':exposed,'minimum_roof_cover_outside_houses_m':min(covers),'outside_parcel_m2':foot.difference(pa).area,'under_future_sidewalk_m2':foot.intersection(strip).area,'level_overlap_excluding_shaft_m2':cfg['levels'][0]['foot'].intersection(cfg['levels'][1]['foot']).difference(shaft.buffer(.25)).area,'different_SS_floor_conflicts':hits,'villa_projected_overlap_m2':foot.intersection(villa).area,'south_house_plan_distance_m':foot.distance(houses[1]),'levels':[]}
 for l in cfg['levels']:
  dct['levels'].append({'z':l['z'],'rooms':[{'home':h,'area':p.area,'polygon':mapping(p)} for h,p in l['rooms']],'man_m2':l['man'].area,'man_polygon':mapping(l['man']),'private_overlap_m2':sum(l['man'].intersection(p).area for _,p in l['rooms']),'table_centres':[t.tolist() for t in l['tables']]})
 diagnostics.append(dct)
check={'sources':hashes,'source_geometry_unchanged':True,'lift':{'shaft':mapping(shaft),'wait':mapping(wait),'wait_m2':wait.area,'shift_north_from_v76_m':.65,'stops':[19.30,16.51,14.56],'pit_bottom':13.96,'top_clearance':2.7,'distance_villa':shaft.distance(villa),'distance_north':shaft.distance(houses[0]),'wait_on_future_sidewalk':wait.intersection(strip).area,'wait_outside_parcel':wait.difference(pa).area},'configs':diagnostics,'vehicle':{'length':5,'width_including_mirrors':2.1,'wheelbase':3,'rear_axle_radius':4.5,'door_opening_check':'Static clearances only; no simultaneous full door opening guarantee','lower_lift_to_table_reverse_adjustment_m':0,'approach_arc_degrees':80}}
# Check exact swept approach against shaft walls and projected constraints, not just a centreline.
shaft_walls=shaft.difference(box(11.3,-5.05,14.1,1.55))
check['vehicle']['lower_approach_shaft_wall_overlap_m2']=sw.intersection(shaft_walls).area
check['vehicle']['lower_approach_north_SS_overlap_m2']=sw.intersection(houses[0]).area
check['vehicle']['lower_approach_villa_projection_overlap_m2']=sw.intersection(villa).area
check['lift']['waiting_clearance_future_alignment_m']=wait.distance(alignment)
check['vehicle']['north_lift_to_table_reverse_centre_distance_m']=float(np.linalg.norm(cn-np.array([12.7,-1.75])))
check['vehicle']['parking_other_car_conflicts']={}
for home,paths in park_paths.items():
 check['vehicle']['parking_other_car_conflicts'][home]=[sweep(path).intersection(car_at(*paths[1-i][-1])).area for i,path in enumerate(paths)]
# Height-band projection of original Villa geometry (not a roof silhouette).
def clipz(poly,z,keepabove):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  ia=a[2]>=z if keepabove else a[2]<=z;ib=b[2]>=z if keepabove else b[2]<=z
  if ia:out.append(a)
  if ia!=ib:
   t=(z-a[2])/(b[2]-a[2]);out.append([a[j]+t*(b[j]-a[j]) for j in range(3)])
 return out
for cfg,dct in zip(configs,diagnostics):
 collisions=[]
 for lev in cfg['levels']:
  for o in G:
   if o['group']!='villa' or o.get('expansion') or o.get('source_group')!='exterior':continue
   vv=o['vertices'];parts=[]
   for f in o['faces']:
    pp=clipz([vv[i] for i in f],lev['z']-19.56,True)
    if pp:pp=clipz(pp,lev['z']+2.55-19.56,False)
    if len(pp)>=3:
     q=Polygon([[-v[1],v[0]] for v in pp])
     if q.area>1e-8:parts.append(q)
   if parts:
    q=unary_union(parts).intersection(lev['foot'])
    if q.area>1e-5:collisions.append({'name':o['name'],'level':lev['z'],'area':q.area})
 dct['villa_height_band_collisions']=collisions
for n,h in hashes.items():assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h
(P/'ESTUDIO_B2-v77-mediciones.json').write_text(json.dumps(check,ensure_ascii=False,indent=2))
print(json.dumps(check,ensure_ascii=False,indent=2)[-2200:])
