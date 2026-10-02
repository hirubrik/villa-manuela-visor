// One state facade over the existing camera and controls; all setters touch only their own property.
function cameraSnapshot(){return {yaw,pitch,distance,target:target.slice(),orthographic,focalMM,cameraHeight,imageOrientation,navigationMode,walking:walkUI.active,walker:walkUI.active?{pos:walkUI.walker.pos.slice(),angle:walkUI.walker.angle,pitch:walkUI.walker.pitch}:null};}
function stateSnapshot(){return {version:state,lighting:lightingMode,context:parcelScope,visibleFloors:floorBoxes.filter(b=>b.checked).map(b=>+b.dataset.level),hiddenFacades:Object.keys(facadeState).filter(k=>!facadeState[k]),separation:+ui.explode.value,mode:ui.mode.value,terrainVisible:ui.context.checked,furnitureVisible:ui.furn.checked,contoursVisible:ui.edges.checked,camera:cameraSnapshot()};}
function refreshSelectors(){for(const[id,v]of [['versionA',state==='actual'],['versionB',state==='reformado'],['scopeA',parcelScope==='environment'],['scopeB',parcelScope==='parcel'],['lightingA',lightingMode==='day'],['lightingB',lightingMode==='night']])document.getElementById(id).setAttribute('aria-pressed',String(v));document.getElementById('modelStatus').textContent=(state==='actual'?'Actual · V79':'Reformada · MASTER')+' · '+(lightingMode==='day'?'Día':'Noche');}
function setViewer(key,value){
 if(key==='version'){if(!['actual','reformado'].includes(value))return;if(state===value)return;state=value;if(walkUI.doors){for(const d of walkUI.doors.doors)for(const o of d.render){gl.deleteBuffer(o.buffer);gl.deleteBuffer(o.edgeBuffer);}walkUI.doors=null;if(walkUI.active){walkUI.doors=new WalkDoors(data,state==='actual'?actualDoorSpecs:doorSpecs,prepareObject);walkUI.world=walkUI.doors.world;walkUI.walker.world=walkUI.world;}}}
 else if(key==='lighting')lightingMode=value;
 else if(key==='context')parcelScope=value;
 else if(key==='separation')ui.explode.value=String(value);
 else if(key==='mode')ui.mode.value=value;
 else if(key==='visibleFloors')floorBoxes.forEach(b=>b.checked=value.includes(+b.dataset.level));
 else if(key==='hiddenFacades'){for(const f of ['N','S','E','O']){facadeState[f]=!value.includes(f);document.getElementById('facade'+f).checked=facadeState[f];}}
 else if(key==='terrainVisible')ui.context.checked=!!value;
 else if(key==='furnitureVisible')ui.furn.checked=!!value;
 else if(key==='contoursVisible')ui.edges.checked=!!value;
 refreshSelectors();update();
}
for(const[id,k,v]of [['versionA','version','actual'],['versionB','version','reformado'],['lightingA','lighting','day'],['lightingB','lighting','night'],['scopeA','context','environment'],['scopeB','context','parcel']])document.getElementById(id).onclick=()=>setViewer(k,v);
window.villaViewer={get state(){return stateSnapshot();},set:setViewer,audit(){const list=displayObjects().filter(visible);return {state:stateSnapshot(),visible:list.length,sourceIndices:[...new Set(list.map(facadeSourceIndex))],externalVisible:list.filter(o=>exteriorIndexSet.has(facadeSourceIndex(o))).length,levels:Object.fromEntries([3,0,1,2,4,5].map(l=>[l,list.filter(o=>o.level===l).length])),clipBands:list.filter(o=>o._clip&&(o._clip[0]>-1e5||o._clip[1]<1e5)).length,lights:nightLights.length,geometryRecords:data.length,glError:window.__villaLastGLError};}};
window.__viewerRuntimeData=()=>({masterCount:viewerMeta.masterCount,sourceGeometry:data.slice(0,viewerMeta.masterCount),conflicts:objects.filter(o=>displayBands(o).length>1).map(o=>({index:o._sourceIndex,name:o.name,levels:displayBands(o).map(b=>b.level)}))});
refreshSelectors();
