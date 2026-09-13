const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const version='77',root=__dirname;
const h=fs.readFileSync(root+'/visor.html','utf8');
const geo=h.match(/<script id="geometry" type="application\/json">([\s\S]*?)<\/script>/)[1];
let code=[...h.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)].filter(m=>!m[1].includes('application/json')).map(m=>m[2]).join('\n');
let id=0,bound=null,uniforms={},enabled=new Set(),depthWrite=true,lastDraws=[],buffers=new Map(),clearColor=[];
const constants={VERTEX_SHADER:35633,FRAGMENT_SHADER:35632,COMPILE_STATUS:35713,LINK_STATUS:35714,ARRAY_BUFFER:34962,STATIC_DRAW:35044,FLOAT:5126,TRIANGLES:4,LINES:1,DEPTH_TEST:2929,CULL_FACE:2884,BLEND:3042,SRC_ALPHA:770,ONE_MINUS_SRC_ALPHA:771,POLYGON_OFFSET_FILL:32823,COLOR_BUFFER_BIT:16384,DEPTH_BUFFER_BIT:256};
const gl=new Proxy({
 getProgramParameter:()=>!process.env.VILLA_FORCE_LINK_ERROR,
 getProgramInfoLog:()=>process.env.VILLA_FORCE_LINK_ERROR?'Fallo de enlace inyectado para prueba':'',
 createBuffer:()=>++id,bindBuffer:(_,b)=>bound=b,
 bufferData:(_,a)=>{for(const n of a)assert(Number.isFinite(n));buffers.set(bound,a)},
 getUniformLocation:(_,name)=>name,getAttribLocation:(_,name)=>name==='position'?0:1,
 uniform1f:(n,v)=>uniforms[n]=v,uniform2f:(n,a,b)=>uniforms[n]=[a,b],
 uniform3fv:(n,v)=>uniforms[n]=Array.from(v),uniformMatrix4fv:(n,_,v)=>uniforms[n]=Array.from(v),
 enable:k=>enabled.add(k),disable:k=>enabled.delete(k),depthMask:b=>depthWrite=b,
 clearColor:(...v)=>clearColor=v,clear:()=>lastDraws=[],getError:()=>0,
 drawArrays:(mode,first,count)=>lastDraws.push({buffer:bound,mode,first,count,depthWrite,blend:enabled.has(constants.BLEND),cull:enabled.has(constants.CULL_FACE),polygonOffset:enabled.has(constants.POLYGON_OFFSET_FILL),uniforms:{...uniforms}}),
}, {get:(t,k)=>k in t?t[k]:k in constants?constants[k]:()=>1});
const elements={};const get=id=>elements[id]??={style:{},value:id==='b2'?'none':id==='b2view'?'context':id==='parking'?'none':id==='expansion'?'none':id==='alignment'?'actual':id==='mode'?'all':id==='explode'?'0':id==='villaState'?'actual':'',checked:id!=='edges',textContent:id==='geometry'?geo:id==='envelope-display'?h.match(/<script id="envelope-display" type="application\/json">([\s\S]*?)<\/script>/)[1]:'',clientWidth:1200,clientHeight:900,listeners:{},addEventListener(t,f,cap=false){(this.listeners[t]??=[]).push({f,cap})},getBoundingClientRect(){return {left:0,top:0,width:1200,height:900}},getContext(){return gl},setPointerCapture(){},focus(){},setAttribute(k,v){this[k]=v},getAttribute(k){return this[k]}};
const boxes=[0,1,2,3,4].map(l=>({...get('level'+l),dataset:{level:String(l)}}));
function dump(name,vert,frag){
 if(!process.env.VILLA_DUMP)return;const used=new Set(lastDraws.map(d=>d.buffer));
 const b=Object.fromEntries([...used].map(k=>[k,Array.from(buffers.get(k))]));
 fs.writeFileSync(__dirname+'/trace-v'+version+'-'+name+'.json',JSON.stringify({width:get('view').clientWidth,height:get('view').clientHeight,clearColor,vert,frag,buffers:b,draws:lastDraws}));
}
function checkGlass(){
 const gd=lastDraws.filter(d=>d.uniforms.exteriorGlass===1&&d.mode===4);
 assert(gd.length===123);assert(gd.every(d=>!d.depthWrite&&d.blend&&!d.cull));
 const start=lastDraws.findIndex(d=>d.blend);
 assert(start>0);assert(lastDraws.slice(start).every(d=>d.blend&&!d.depthWrite));
 assert(lastDraws.slice(0,start).every(d=>d.depthWrite&&!d.blend));
 assert(depthWrite===true&&!enabled.has(constants.BLEND));
 assert(gd.every(d=>d.uniforms.opacity===.04&&d.uniforms.glassReflectance[1]===.24));
}
const docListeners={},winListeners={};
const fire=(id,type,e={})=>{const ev={target:get(id),preventDefault(){},...e};for(const l of (get(id).listeners[type]||[]).slice().sort((a,b)=>Number(b.cap)-Number(a.cap)))l.f(ev);};
const fireKey=(type,code,extra={})=>docListeners[type].forEach(f=>f({code,target:{tagName:'CANVAS'},preventDefault(){},...extra}));
const sandbox={getDraws:()=>lastDraws,fire,fireKey,winListeners,setTimeout:f=>f(),performance:{now:()=>100},requestAnimationFrame:()=>1,cancelAnimationFrame:()=>{},document:{getElementById:get,querySelectorAll:()=>boxes,addEventListener:(t,f)=>(docListeners[t]??=[]).push(f)},window:{addEventListener:(t,f)=>winListeners[t]=f},ResizeObserver:class{observe(){}},devicePixelRatio:1,assert,console,dump,checkGlass,version,routes:{},writeReport:(name,r)=>fs.writeFileSync(__dirname+'/'+name,JSON.stringify(r,null,2))};

code=code.replace('window.__baseReady=true;',`window.__baseReady=true;assert(document.getElementById('b2').value==='none');draw();assert(getDraws().length===4040);
for(const a of ['actual','hypothesis'])for(const b of ['B2-1','B2-2'])for(const v of ['context','alto','bajo','all']){document.getElementById('alignment').value=a;document.getElementById('b2').value=b;document.getElementById('b2view').value=v;changeB2();assert(getDraws().length===objects.filter(isVisible).length);assert(getDraws().length>0);assert(getDraws().every(d=>d.uniforms.mvp.every(Number.isFinite)));if(v!=='context')assert(objects.filter(isVisible).every(o=>o.b2===b));}
document.getElementById('b2').value='B2-1';document.getElementById('alignment').value='hypothesis';for(const v of ['alto','bajo','all','context']){document.getElementById('b2view').value=v;changeB2();dump(v,vert,frag);}
document.getElementById('b2').value='none';document.getElementById('alignment').value='actual';document.getElementById('expansion').value='none';draw();assert(getDraws().length===4040);writeReport('viewer-test.json',{defaultNone:true,sixteenVariantCombinations:true,baseRestored:true,finiteMatrices:true});
`);vm.runInNewContext(code,sandbox,{timeout:120000});assert(sandbox.window.__baseReady===true);console.log('PASS V77');