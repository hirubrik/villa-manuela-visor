// Display metadata and GPU clipping only. Source arrays are never edited.
const exteriorIndexSet=new Set(viewerMeta.outer),fixtureIndexSet=new Set(viewerMeta.fixtures);
const floorBands=[{level:3,lo:-1e5,hi:-.25},{level:0,lo:-.25,hi:3.28},{level:1,lo:3.28,hi:6.65},{level:2,lo:6.65,hi:1e5}];
function furnishings(o){return /(?:V106_|V111_|mobiliario|cocina_|isla_|mesa_|sofa_|butaca|sillon|cama_|armario|libreria|estanteria|alfombra|cojin|banqueta|taburete|silla_|television|tv_|fregadero|lavabo|inodoro|sanitario)/i.test(o.name);}
function displayBands(o){
 if(!o.vertices.length||!o.faces.length)return [];
 if(o.level===5||fixtureIndexSet.has(o._sourceIndex))return [{...o,_clip:[-1e5,1e5]}];
 const n=o.name.toLowerCase(),roof=o.level===4&&!/fachada|hueco|cerco|despiece|ornamento|bandas|retorno|pilastra|solarium|marco|vidrio|carpinteria/.test(n);
 if(roof||furnishings(o))return [{...o,_clip:[-1e5,1e5]}];
 let lo=Infinity,hi=-Infinity;for(const v of o.vertices){lo=Math.min(lo,v[2]);hi=Math.max(hi,v[2]);}
 const exterior=o.group==='exterior';
 if(!exterior&&hi-lo<2.8)return [{...o,_clip:[-1e5,1e5]}];
 const bands=floorBands.filter(b=>hi>b.lo+.0001&&lo<b.hi-.0001);
 if(!bands.length)return [{...o,_clip:[-1e5,1e5]}];
 return bands.map(b=>({...o,level:b.level,_clip:[b.lo,b.hi]}));
}
const storeyObjects=objects.flatMap(displayBands);
function displayObjects(){
 if(walkUI.active&&walkUI.doors)return walkUI.doors.renderObjects(objects).flatMap(displayBands);
 // Gate animation may replace buffers without changing the master.
 return storeyObjects.map(o=>o._sourceIndex>=7652&&o._sourceIndex<=7677?{...objects[o._sourceIndex],_clip:o._clip,level:o.level}:o);
}
