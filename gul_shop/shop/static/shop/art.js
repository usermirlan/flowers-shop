/* Сүрөт жок товарлар үчүн тартылган гүлдөр */

function rnd(seed){let s=seed;return()=>{s=(s*9301+49297)%233280;return s/233280}}
function shade(hex,a){const n=parseInt(hex.slice(1),16);let r=n>>16,g=(n>>8)&255,b=n&255;r=Math.max(0,Math.min(255,r+a));g=Math.max(0,Math.min(255,g+a));b=Math.max(0,Math.min(255,b+a));return"#"+((1<<24)+(r<<16)+(g<<8)+b).toString(16).slice(1)}
function head(t,x,y,r,c,R){
 if(t==="rose"){const d=shade(c,-38);return`<g><circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/><circle cx="${x}" cy="${y}" r="${r*.98}" fill="none" stroke="${shade(c,-20)}" stroke-width="1"/><path d="M${x-r*.62} ${y+r*.1} a${r*.62} ${r*.62} 0 1 1 ${r*.95} ${r*.45}" fill="none" stroke="${d}" stroke-width="1.5"/><path d="M${x-r*.32} ${y-r*.05} a${r*.34} ${r*.34} 0 1 1 ${r*.5} ${r*.28}" fill="none" stroke="${d}" stroke-width="1.4"/><circle cx="${x+r*.05}" cy="${y}" r="${r*.13}" fill="${d}"/></g>`}
 if(t==="tulip"){const d=shade(c,-30);return`<g><path d="M${x-r} ${y-r*.35} Q${x-r} ${y+r} ${x} ${y+r} Q${x+r} ${y+r} ${x+r} ${y-r*.35} L${x+r*.5} ${y-r*.9} L${x} ${y-r*.25} L${x-r*.5} ${y-r*.9} Z" fill="${c}" stroke="${d}" stroke-width="1"/><path d="M${x} ${y-r*.25} Q${x-r*.15} ${y+r*.5} ${x} ${y+r}" stroke="${d}" fill="none" stroke-width="1"/></g>`}
 if(t==="peony"){let s="";for(let i=0;i<7;i++){const a=i/7*Math.PI*2,o=r*.45;s+=`<circle cx="${x+Math.cos(a)*o}" cy="${y+Math.sin(a)*o}" r="${r*.6}" fill="${shade(c,-10+i*3)}"/>`}for(let i=0;i<5;i++){const a=i/5*Math.PI*2+.4,o=r*.22;s+=`<circle cx="${x+Math.cos(a)*o}" cy="${y+Math.sin(a)*o}" r="${r*.42}" fill="${shade(c,12)}" stroke="${shade(c,-15)}" stroke-width=".6"/>`}return`<g>${s}<circle cx="${x}" cy="${y}" r="${r*.2}" fill="${shade(c,25)}"/></g>`}
 if(t==="daisy"){let s="";for(let i=0;i<12;i++){const a=i/12*360;s+=`<ellipse cx="${x}" cy="${y-r*.58}" rx="${r*.2}" ry="${r*.48}" fill="#fff" stroke="#e5ded0" stroke-width=".6" transform="rotate(${a} ${x} ${y})"/>`}return`<g>${s}<circle cx="${x}" cy="${y}" r="${r*.32}" fill="#f2b822"/><circle cx="${x}" cy="${y}" r="${r*.32}" fill="none" stroke="#d99a10" stroke-width="1"/></g>`}
 if(t==="chrys"){let s="";for(let i=0;i<18;i++){const a=i/18*360;s+=`<ellipse cx="${x}" cy="${y-r*.55}" rx="${r*.13}" ry="${r*.45}" fill="${c}" stroke="${shade(c,-25)}" stroke-width=".5" transform="rotate(${a} ${x} ${y})"/>`}return`<g>${s}<circle cx="${x}" cy="${y}" r="${r*.3}" fill="${shade(c,-20)}"/></g>`}
 return""}
function bouquet(a,seed){
 if(a.t==="straw")return strawBox();
 const R=rnd(seed),cx=100,cy=95,heads=[],n=a.n;
 const t=a.t==="combo"?"rose":a.t;
 for(let i=0;i<n;i++){const ang=Math.PI+(i/(n-1||1))*Math.PI,ring=i%2?0.55:1;let rr=48*(i===0?0:Math.sqrt((i+.5)/n));const th=i*2.4;heads.push({x:cx+Math.cos(th)*rr*1.15,y:cy+Math.sin(th)*rr*.75,r:(t==="peony"?20:t==="tulip"?13:t==="daisy"?15:14)+R()*3})}
 heads.sort((p,q)=>p.y-q.y);
 const wrap=a.wrap||"#efe6da",wd=shade(wrap,-22);
 let s=`<svg viewBox="0 0 200 230" xmlns="http://www.w3.org/2000/svg">`;
 // back wrap
 s+=`<path d="M28 98 L100 222 L172 98 Q150 78 100 84 Q50 78 28 98Z" fill="${wd}"/>`;
 // leaves
 for(let i=0;i<9;i++){const ang=-160+i*17+R()*8,lx=cx+Math.cos(ang*Math.PI/180)*62,ly=cy+18+Math.sin(ang*Math.PI/180)*40;s+=`<ellipse cx="${lx}" cy="${ly}" rx="7" ry="20" fill="${i%2?'#3f6b4c':'#557f5e'}" transform="rotate(${ang+90} ${lx} ${ly})"/>`}
 if(a.t==="mix"||a.t==="combo"){for(let i=0;i<6;i++){const lx=cx-60+i*24,ly=cy-38+R()*14;s+=`<circle cx="${lx}" cy="${ly}" r="3.5" fill="#9bb7a2"/><circle cx="${lx+5}" cy="${ly+7}" r="3.5" fill="#8aa893"/>`}}
 heads.forEach((h,i)=>{let tt=t,c=a.c[i%a.c.length];if(a.t==="mix"){tt=["rose","chrys","daisy","rose"][i%4];c=a.c[i%a.c.length];if(tt==="chrys")c="#f4c542"}s+=head(tt,h.x,h.y,h.r,c,R)});
 // front wrap
 s+=`<path d="M38 118 L100 224 L162 118 L130 132 L100 126 L70 132Z" fill="${wrap}" stroke="${wd}" stroke-width="1"/>`;
 s+=`<path d="M70 132 L100 224 M130 132 L100 224" stroke="${wd}" stroke-width="1" opacity=".6"/>`;
 // ribbon
 s+=`<path d="M100 176 q-22 -14 -26 2 q4 12 26 -2z M100 176 q22 -14 26 2 q-4 12 -26 -2z" fill="#d4577a"/><circle cx="100" cy="176" r="5" fill="#b8405f"/><path d="M98 180 l-8 22 M102 180 l8 22" stroke="#d4577a" stroke-width="3" stroke-linecap="round"/>`;
 if(a.t==="combo"){s+=`<g transform="translate(118 150) scale(.42)">${strawInner()}</g>`}
 return s+"</svg>"}
function strawInner(){let s=`<rect x="10" y="60" width="160" height="110" rx="10" fill="#f7d9e1" stroke="#e7b3c2" stroke-width="2"/><rect x="10" y="60" width="160" height="22" rx="8" fill="#d4577a"/>`;
 const pos=[[40,110],[80,105],[120,110],[150,112],[55,145],[95,142],[135,145]];
 pos.forEach(([x,y],i)=>{s+=`<path d="M${x-15} ${y-6} Q${x} ${y+30} ${x+15} ${y-6} Q${x} ${y-16} ${x-15} ${y-6}Z" fill="#e0263e"/><path d="M${x-15} ${y-6} Q${x} ${y+14} ${x+15} ${y-6} Q${x} ${y-16} ${x-15} ${y-6}Z" fill="${i%3===1?'#f4ead8':'#4a2a1c'}"/>${i%3===1?'':`<path d="M${x-10} ${y+2} l20 -3 M${x-8} ${y+7} l16 -3" stroke="#f4ead8" stroke-width="1.6"/>`}<path d="M${x-6} ${y-14} l6 6 l6 -6" stroke="#3f6b4c" stroke-width="3" fill="none"/>`});
 return s}
function strawBox(){return`<svg viewBox="0 0 180 200" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0 10)">${strawInner()}</g><path d="M90 42 q-18 -16 -26 0 q8 10 26 0z M90 42 q18 -16 26 0 q-8 10 -26 0z" fill="#d4577a"/><circle cx="90" cy="42" r="5" fill="#b8405f"/></svg>`}

