function visible(o){
 if(!isStateActive(o))return false;
 if(fixtureIndexSet.has(facadeSourceIndex(o))&&lightingMode!=='night')return false;
 if(parcelScope==='parcel'&&exteriorIndexSet.has(facadeSourceIndex(o)))return false;
 if(facadeState[facadeFor(o)]===false||!variantVisible(o))return false;
 if(!ui.furn.checked&&furnishings(o))return false;
 const mode=ui.mode.value;
 if(o.level===5)return ui.context.checked;
 if(!floorBoxes.find(b=>+b.dataset.level===o.level)?.checked)return false;
 if(mode==='stairs')return /escalera|barandilla|descansillo/.test(o.name);
 if(mode==='roof'&&o.level!==4)return false;
 if(!['all','roof'].includes(mode)&&o.level!==+mode)return false;
 return true;
}
function offset(o){const ex=+ui.explode.value;return o.level===4?ex*3:o.level===5?0:o.level===3?-ex:ex*o.level;}
