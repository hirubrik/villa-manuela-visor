from pathlib import Path
import json,re,hashlib,collections
P=Path.cwd();A=P/'auxiliar-visor-definitivo';master=P/'VILLA_MANUELA_REFORMADA_MASTER_FINAL.html';h=master.read_text();hist=(P/'V70_TECNICA-v79.html').read_text();night=(P/'V70_REFORMADA_ENTORNO_ILUMINACION-v105.html').read_text();out=P/'VILLA_MANUELA_VISOR_DEFINITIVO-v112.html'
def geom(s):return json.loads(re.search(r'<script id="geometry" type="application/json">(.*?)</script>',s,re.S)[1])
def const(s,n):return json.JSONDecoder().raw_decode(s.split('const '+n+'=',1)[1])[0]
D=geom(h);baseCount=len(D);H=geom(hist);hs=const(hist,'villaStates')['actual'];ND=geom(night);index={hashlib.sha256(json.dumps(o,sort_keys=True).encode()).hexdigest():i for i,o in enumerate(D)};actual=[];histMap={};facades=const(h,'facadeByIndex');hf=const(hist,'facadeByIndex');facades+= [None]*(len(D)-len(facades));fixtures=[]
for j in hs:
 o=H[j];key=hashlib.sha256(json.dumps(o,sort_keys=True).encode()).hexdigest();i=index.get(key)
 if i is None:i=len(D);D.append(o);index[key]=i;facades.append(hf[j] if j<len(hf)else None)
 actual.append(i);histMap[j]=i
for o in ND:
 if o['name'].startswith('NOCTURNA_'):fixtures.append(len(D));D.append(o);facades.append(None)
def external(o):
 n=o['name'].lower();return n.startswith('entorno_v99_') or n.startswith('entorno_v100_') or n.startswith('entorno_v101_') or n.startswith('entorno_v103_') or any(x in n for x in ['carretera_norte','acera_norte','bordillo_norte'])
outer=[i for i,o in enumerate(D)if external(o)];actual=list(dict.fromkeys(actual+[i for i in outer if i<baseCount and not D[i]['name'].startswith('entorno_v49_')]+fixtures));reform=list(range(baseCount))+fixtures
# Keep exact original master payload as immutable separate reference; combined payload simply references original records.
h=re.sub(r'(<script id="geometry" type="application/json">).*?(</script>)',lambda m:m[1]+json.dumps(D,separators=(',',':'))+m[2],h,count=1,flags=re.S)
for name,value in [('villaStates',{'actual':actual,'reformado':reform}),('facadeByIndex',facades)]:h=re.sub(r'(const '+name+r'=).*?;',lambda m:m[1]+json.dumps(value,separators=(',',':'))+';',h,count=1)
# Fill historically missing explicit facade labels (stair tower and upper returns).
for i,o in enumerate(D):
 if facades[i] is None and o.get('group')=='exterior' and o.get('level')!=5:
  n=o['name'].lower()
  if not any(k in n for k in ['cubierta','tejado','alero','canalon','cumbrera']):
   for word,side in [('norte','N'),('sur','S'),('este','E'),('oeste','O')]:
    if re.search(r'(^|_)'+word+r'(_|$)',n):facades[i]=side;break
h=re.sub(r'(const facadeByIndex=).*?;',lambda m:m[1]+json.dumps(facades,separators=(',',':'))+';',h,count=1)
# Extract existing camera UI / floors / facades instead of changing identity.
oldUI=h[h.index('<header>'):h.index('<script id="envelope-display"')]
cam=re.search(r'<div id="interiorCameraControls".*?</p></div>',oldUI,re.S)[0].replace('<h2>CÁMARA INTERIOR</h2>','')
sections=re.findall(r'<section>.*?</section>',oldUI,re.S);floors=next(s for s in sections if '<h2>PLANTAS</h2>'in s);fac=next(s for s in sections if '<h2>FACHADAS</h2>'in s);vis=next(s for s in sections if '<h2>VISUALIZACIÓN</h2>'in s)
sep=re.search(r'<div class="temporary">.*?</div></div>',oldUI,re.S)[0];sep=sep.replace('class="temporary"','class="separation-controls"').replace('class="popover"','class="separation-slider"')
floors=floors.replace('</section>',sep+'</section>')
def pair(title,id,a,b):return f'<section><h2>{title}</h2><div class="selector" role="group" aria-label="{title}"><button id="{id}A">{a}</button><button id="{id}B">{b}</button></div></section>'
panel=pair('VERSIÓN','version','ACTUAL','REFORMADA')+pair('ILUMINACIÓN','lighting','DÍA','NOCHE')+pair('CONTEXTO','scope','ENTORNO','SOLO PARCELA')+f'<section><h2>CÁMARA Y CAPTURA</h2><label>Formato</label><button id="imageOrientation">Horizontal 4:3</button>{cam}<div class="capture-controls"><button id="cleanCapture">Captura limpia</button><button id="fullscreen">Pantalla completa</button><button id="reset">Restablecer cámara</button></div></section>'+floors+fac+vis
# Replace UI only, retain canvas/walk tools.
stage=oldUI[oldUI.index('<main>'):oldUI.index('<aside')];stage=stage.replace(re.search(r'<div class="temporary">.*?</div></div>',stage,re.S)[0],'');stage=stage.replace('Elige una vista interior y pulsa Recorrer para caminar desde allí.','Pulsa Recorrer para caminar por la casa.')
ui='<header><div class="brand"><h1>VILLA MANUELA</h1><span class="sub">Modelo 3D</span></div><span class="version" id="modelStatus">Visor definitivo</span><button id="panelToggle" aria-label="Mostrar u ocultar controles">☷</button></header>'+stage+'<aside id="controls" data-closed="true">'+panel+'</aside></main><footer><strong id="status"></strong><span id="detail"></span><div class="links"><a href="VILLA_MANUELA_VISOR_DEFINITIVO-v112_REGISTRO.md">Notas</a><button id="helpToggle" class="text-button">Ayuda</button></div></footer>\n'
h=h.replace(oldUI,ui).replace('<title>VILLA_MANUELA_REFORMADA_MASTER_FINAL</title>','<title>VILLA MANUELA — Visor definitivo</title>')
h=h.replace('</style>','.selector{display:flex;gap:5px}.selector button{flex:1;font-size:11px;padding:6px}.selector button[aria-pressed=true]{background:#365c50;color:white}.capture-controls{display:flex;gap:5px;flex-wrap:wrap}.capture-controls button,#imageOrientation{font-size:11px;margin-top:5px}.separation-controls{margin-top:8px}.separation-slider{padding:8px 0}aside h2{font-size:10px}main{grid-template-columns:minmax(0,1fr) 260px}</style>',1)
# Remove obsolete view/save/route logic entirely.
h=re.sub(r'// Existing controls keep their behaviour;.*?function variantVisible', 'function variantVisible',h,flags=re.S)
lines=h.splitlines();kill=['document.getElementById(\'interiorPB\').onclick','document.getElementById(\'interiorP1\').onclick','document.getElementById(\'interiorP2\').onclick','document.getElementById(\'interiorSS\').onclick','document.getElementById(\'persp\').onclick','document.getElementById(\'top\').onclick','function elevation(',"document.getElementById('garden').onclick",'for(const id of [\'reset\',\'interiorPB\'',"document.getElementById('exteriorViews').onchange","document.getElementById('interiorViews').onchange","ui.mode.addEventListener('input',()=>{interiorStart=null;"]
h='\n'.join(l for l in lines if not any(l.startswith(k)for k in kill))
h=re.sub(r'const interiorPresets=.*?function interiorView\(key\).*?return true;}','',h,flags=re.S)
h=re.sub(r"const cameraKey=.*?document.getElementById\('eyeHeight'\).addEventListener", "document.getElementById('eyeHeight').addEventListener",h,flags=re.S)
h=re.sub(r"document.getElementById\('cameraSave'\).onclick=.*?refreshCameras\(\);",'',h,flags=re.S) if False else h
start=h.index("document.getElementById('cameraSave').onclick=");end=h.index('let cleanCapture=',start);h=h[:start]+h[end:]
# Preserve gate animation behind API, remove UI button.
h=re.sub(r"document.getElementById\('parkingGate'\).onclick=.*?draw\(\);};", "window.setParkingGate=open=>{parkingGateOpen=!!open;parkingGateIndices.forEach((idx,j)=>objects[idx]=parkingGateOpen?parkingOpen[j]:parkingClosed[j]);draw();};",h)
# Night shader recovered unchanged except display-only floor clipping.
nfrag=night[night.index('const frag='):night.index('function shader(')]
nfrag=nfrag.replace('varying vec3 n;','uniform vec2 displayClip;varying vec3 n;',1).replace('void main(){','void main(){if(surfacePosition.z<displayClip.x||surfacePosition.z>=displayClip.y)discard;',1)
h=h[:h.index('const frag=')]+nfrag+h[h.index('function shader('):]
# Reuse buffers for display bands; no new vertices or faces.
a=h.index('// V03 groups');b=h.index('function multiply(',a)
clip=h[h.index('function clipPolygon(',a):h.index('function segmentExterior(',a)]
h=h[:a]+clip+(A/'classification.js').read_text()+h[b:]
# Replace visibility and offsets with state-driven implementation.
a=h.index('function visible(o)');b=h.index('function frame()',a);h=h[:a]+(A/'visibility.js').read_text()+h[b:]
h=h.replace("if(id==='mode'||id==='explode')frame();",'').replace("const level=ui.mode.value==='roof'?4:+ui.mode.value;const box=floorBoxes.find(b=>+b.dataset.level===level);if(box)box.checked=true;",'')
h=h.replace("ui.explode.disabled=ui.mode.value!=='all';","ui.explode.disabled=false;")
h=h.replace("ui.mode.value!=='all'?'Separación disponible en «Todas las plantas»':",'')
h=re.sub(r"document.getElementById\('reset'\).onclick=.*?;\n", "document.getElementById('reset').onclick=()=>{yaw=-2.42;pitch=.38;distance=44;target=[0,0,4];orthographic=false;draw();};\n",h,count=1)
h=h.replace("document.getElementById('separatePanel').hidden=true;document.getElementById('separateToggle').setAttribute('aria-expanded','false');", "ui.explode.value='0';document.getElementById('separatePanel').hidden=true;document.getElementById('separateToggle').setAttribute('aria-expanded','false');update();")
# Night runtime, plus shadows follow displayed model and floor clipping.
runtime=night[night.index('const nightLights='):night.index('function draw()')]
runtime=runtime.replace("document.getElementById('lightingDay')","document.getElementById('lightingA')").replace("document.getElementById('lightingNight')","document.getElementById('lightingB')")
old="const triangles=[];for(const o of objects){if(!isStateActive(o)||isTransparent(o)||o.name.startsWith('NOCTURNA_'))continue;for(const f of o.faces)for(const j of f)triangles.push(...o.vertices[j]);}"
new="const triangles=[];for(const o of displayObjects()){if(!visible(o)||isTransparent(o)||o.name.startsWith('NOCTURNA_'))continue;for(const f of o.faces){const poly=clipPolygon(clipPolygon(f.map(j=>o.vertices[j]),o._clip?.[0]??-1e5,true),o._clip?.[1]??1e5,false);for(let j=1;j+1<poly.length;j++)for(const v of [poly[0],poly[j],poly[j+1]])triangles.push(v[0],v[1],v[2]+offset(o));}}"
assert old in runtime;runtime=runtime.replace(old,new)
runtime=runtime.replace('function ensureNightShadows(){',"let shadowStateKey='';function ensureNightShadows(){const key=JSON.stringify([state,parcelScope,ui.mode.value,ui.explode.value,ui.context.checked,ui.furn.checked,floorBoxes.map(b=>b.checked),facadeState]);if(key!==shadowStateKey){if(nightAtlas)gl.deleteTexture(nightAtlas);if(nightShadowBuffer)gl.deleteBuffer(nightShadowBuffer);if(nightShadowProgram)gl.deleteProgram(nightShadowProgram);nightShadowReady=false;shadowStateKey=key;}")
h=h.replace('function draw(){',runtime+'function draw(){',1)
prefix=night[night.index('function draw(){'):night.index('let w=canvas.clientWidth',night.index('function draw(){'))]
h=h.replace('function draw(){let w=',prefix+'let w=',1).replace('function draw(){ensureNightShadows();','function draw(){if(lightingMode===\'night\')ensureNightShadows();',1)
h=h.replace('gl.clearColor(.945,.94,.915,1);',"lightingMode==='night'?gl.clearColor(.025,.045,.08,1):gl.clearColor(.945,.94,.915,1);",1)
h=h.replace("target[2]+(ui.mode.value==='all'?ex:0)","target[2]")
h=h.replace("(walkUI.active?walkUI.doors.renderObjects(objects):(isExploring()?storeyObjects:objects))","displayObjects()")
h=h.replace('let dz=offset(o);','let dz=offset(o);gl.uniform2fv(gl.getUniformLocation(program,"displayClip"),o._clip||[-1e5,1e5]);')
# Context metadata and central API are external to immutable geometry.
meta={'masterCount':baseCount,'outer':outer,'fixtures':fixtures,'actualIndices':actual,'reformedIndices':reform}
h=h.replace("'use strict';","'use strict';\nconst viewerMeta="+json.dumps(meta,separators=(',',':'))+";let parcelScope='environment';")
h=h.replace('window.__villaReady=true;frame();update();',(A/'state.js').read_text()+'\nwindow.__villaReady=true;frame();update();')
# Reuse each version's existing door articulation and procedural material metadata.
actualDoors=[]
for spec in const(hist,'doorSpecs'):
 if all(i in histMap for i in spec['indices']):
  actualDoors.append({**spec,'indices':[histMap[i] for i in spec['indices']]})
h=h.replace('const walkUI={', 'const actualDoorSpecs='+json.dumps(actualDoors,separators=(',',':'))+';\nconst walkUI={')
h=h.replace('new WalkDoors(data,doorSpecs,prepareObject)',"new WalkDoors(data,state==='actual'?actualDoorSpecs:doorSpecs,prepareObject)")
h=h.replace("ui.mode.value='all';ui.explode.value='0';floorBoxes.forEach(b=>b.checked=true);ui.furn.checked=true;ui.context.checked=true;orthographic=false;","orthographic=false;")
h=h.replace("ui.mode.value=s.mode;ui.explode.value=s.explode;floorBoxes.forEach((b,i)=>b.checked=s.checks[i]);ui.furn.checked=s.furn;ui.context.checked=s.context;",'')
h=h.replace('const finish=interiorStyles[o.name];',"const finish=(state==='actual'?actualInteriorStyles:interiorStyles)[o.name];")
h=h.replace('const walkUI={','const actualInteriorStyles='+json.dumps(const(hist,'interiorStyles'),separators=(',',':'))+';\nconst walkUI={')
h=h.replace('...this.meshes[i],_doorId:d.id','...this.meshes[i],_sourceIndex:i,_doorId:d.id')
out.write_text(h)
assert geom(h)[:baseCount]==geom(master.read_text())
report={'master':master.name,'actual':'V70_TECNICA-v79.html','night':'V70_REFORMADA_ENTORNO_ILUMINACION-v105.html','master_records':baseCount,'actual_records':len(hs),'shared_reused':sum(i<baseCount for i in actual),'display_pool':len(D),'night_fixtures':len(fixtures),'sha256_master':hashlib.sha256(master.read_bytes()).hexdigest(),'file':out.name}
(A/'fuentes.json').write_text(json.dumps(report,indent=2));print(report)
