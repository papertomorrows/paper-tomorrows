const { chromium } = require('playwright'); const fs=require('fs'); const D=__dirname;
let seed=7; const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647};
function stars(w,h,n,maxr,col='255,236,200'){let s='';for(let i=0;i<n;i++){const r=(rnd()**3)*maxr+0.4;const o=(0.25+rnd()*0.75).toFixed(2);s+=`<circle cx="${(rnd()*w).toFixed(1)}" cy="${(rnd()*h).toFixed(1)}" r="${r.toFixed(2)}" fill="rgba(${col},${o})"/>`;}return `<svg width="${w}" height="${h}" style="position:absolute;inset:0">${s}</svg>`;}
const css=`
@font-face{font-family:Corm;src:url(CormorantGaramond.ttf)}@font-face{font-family:CormI;src:url(CormorantGaramond-Italic.ttf)}
@font-face{font-family:Gowun;src:url(GowunBatang-Regular.ttf)}@font-face{font-family:GowunB;src:url(GowunBatang-Bold.ttf)}
@font-face{font-family:Inter;src:url(Inter.ttf)}@font-face{font-family:Pre;src:url(Pretendard-Light.otf)}
*{margin:0;padding:0;box-sizing:border-box}body{width:var(--w);height:var(--h);overflow:hidden;background:#000}
.c{position:relative;width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden}
.grain{position:absolute;inset:0;opacity:.10;mix-blend-mode:overlay;pointer-events:none;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
`;
// warm night bg
const night=(cx='50%',cy='62%')=>`background:radial-gradient(ellipse 75% 65% at ${cx} ${cy},#7a3b2a 0%,#4a2033 32%,#24122a 62%,#130a18 100%)`;
const G='#f2c98a', G2='#ffe2b0';
// motifs (viewBox 0..100)
const arch=(glow=true)=>`<svg viewBox="0 0 100 100" width="100%" height="100%">
<defs><radialGradient id="ag" cx="50%" cy="75%" r="60%"><stop offset="0" stop-color="#fff1d0"/><stop offset=".35" stop-color="#ffc77a"/><stop offset="1" stop-color="#ff9a5a" stop-opacity="0"/></radialGradient>
<linearGradient id="fl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd79a" stop-opacity=".0"/><stop offset="1" stop-color="#ffd79a" stop-opacity=".55"/></linearGradient></defs>
${glow?'<ellipse cx="50" cy="62" rx="34" ry="34" fill="url(#ag)" opacity=".45"/>':''}
<path d="M34 80 L34 44 A16 16 0 0 1 66 44 L66 80 Z" fill="url(#ag)" opacity=".95"/>
<path d="M30 80 L30 43 A20 20 0 0 1 70 43 L70 80" fill="none" stroke="${G}" stroke-width=".8"/>
<polygon points="34,80 66,80 80,92 20,92" fill="url(#fl)"/>
<line x1="14" y1="80" x2="86" y2="80" stroke="${G}" stroke-width=".5" opacity=".7"/>
<g fill="#2a1424"><circle cx="50" cy="66.2" r="1.9"/><path d="M47.6 79.6 L48.3 70 Q50 68.6 51.7 70 L52.4 79.6 Z"/></g>
<circle cx="50" cy="20" r="1.1" fill="${G2}"/></svg>`;
const eclipse=`<svg viewBox="0 0 100 100" width="100%" height="100%"><defs>
<radialGradient id="co" cx="50%" cy="50%" r="50%"><stop offset=".5" stop-color="#ffd697" stop-opacity=".95"/><stop offset=".66" stop-color="#ff9a5a" stop-opacity=".38"/><stop offset="1" stop-color="#ff7a4a" stop-opacity="0"/></radialGradient>
<radialGradient id="dr" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fffaf0"/><stop offset=".3" stop-color="#ffe2a8" stop-opacity=".9"/><stop offset="1" stop-color="#ffb070" stop-opacity="0"/></radialGradient></defs>
<circle cx="50" cy="50" r="42" fill="url(#co)"/><circle cx="50" cy="50" r="23.5" fill="#1d0f1f"/>
<circle cx="50" cy="50" r="23.5" fill="none" stroke="#ffeccb" stroke-width=".7" opacity=".9"/>
<circle cx="33.4" cy="66.6" r="6" fill="url(#dr)"/><circle cx="33.4" cy="66.6" r="1.3" fill="#fffaf0"/></svg>`;
const seedLife=`<svg viewBox="0 0 100 100" width="100%" height="100%"><g fill="none" stroke="${G}" stroke-width=".55" opacity=".95">
<circle cx="50" cy="50" r="13"/>${[0,60,120,180,240,300].map(a=>`<circle cx="${(50+13*Math.cos(a*Math.PI/180)).toFixed(2)}" cy="${(50+13*Math.sin(a*Math.PI/180)).toFixed(2)}" r="13"/>`).join('')}
<circle cx="50" cy="50" r="26"/><circle cx="50" cy="50" r="30" opacity=".5"/></g>
<circle cx="50" cy="50" r="4.5" fill="#ffe7b8"/><circle cx="50" cy="50" r="9" fill="#ffc77a" opacity=".25"/></svg>`;
const sunEye=`<svg viewBox="0 0 100 100" width="100%" height="100%"><g stroke="${G}" stroke-width=".6" fill="none">
${Array.from({length:24},(_,i)=>{const a=i*15*Math.PI/180,r1=27,r2=i%2?33:38;return `<line x1="${(50+r1*Math.cos(a)).toFixed(2)}" y1="${(50+r1*Math.sin(a)).toFixed(2)}" x2="${(50+r2*Math.cos(a)).toFixed(2)}" y2="${(50+r2*Math.sin(a)).toFixed(2)}"/>`}).join('')}
<circle cx="50" cy="50" r="23"/><path d="M33 50 Q50 36 67 50 Q50 64 33 50 Z"/></g><circle cx="50" cy="50" r="5.5" fill="#ffd79a"/><circle cx="50" cy="50" r="2.2" fill="#2a1424"/></svg>`;
const logos={
 "1_golden_door":`<div class="c" style="${night('50%','70%')}">${stars(800,800,90,1.6)}<div style="position:relative;width:760px;height:760px;margin-top:40px">${arch()}</div><div class="grain"></div></div>`,
 "2_eclipse":`<div class="c" style="${night('50%','50%')}">${stars(800,800,80,1.5)}<div style="position:relative;width:700px;height:700px">${eclipse}</div><div class="grain"></div></div>`,
 "3_seed_of_life":`<div class="c" style="${night('50%','50%')}">${stars(800,800,70,1.4)}<div style="position:relative;width:720px;height:720px">${seedLife}</div><div class="grain"></div></div>`,
 "4_sun_eye":`<div class="c" style="background:radial-gradient(circle at 50% 50%,#8a4a30,#4a2033 55%,#1c0e1e)">${stars(800,800,40,1.2)}<div style="position:relative;width:720px;height:720px">${sunEye}</div><div class="grain"></div></div>`,
};
const W=2560,H=1440;
const tE=`<div style="font-family:Corm;font-weight:400;font-size:150px;color:#fbead0;letter-spacing:3px;text-shadow:0 0 40px rgba(255,190,120,.35)">Play Your <span style="font-family:CormI;color:${G}">Own</span> Game</div><div style="font-family:Inter;font-weight:400;font-size:30px;letter-spacing:16px;color:rgba(251,234,208,.7);margin-top:22px">MIND · SOUL · UNIVERSE</div>`;
const tK=`<div style="font-family:Gowun;font-size:140px;color:#fbead0;letter-spacing:10px;text-shadow:0 0 40px rgba(255,190,120,.35)">당신만의 <span style="color:${G}">게임</span></div><div style="font-family:Pre;font-size:38px;letter-spacing:18px;color:rgba(251,234,208,.7);margin-top:26px">마음 · 영혼 · 우주</div>`;
const row=(icon,size,t)=>`<div style="position:relative;display:flex;align-items:center;gap:70px"><div style="width:${size}px;height:${size}px">${icon}</div><div style="text-align:left">${t}</div></div>`;
const bans={
 door:t=>`<div class="c" style="${night('50%','58%')}">${stars(W,H,420,2.2)}${row(arch(true),400,t)}<div class="grain"></div></div>`,
 eclipse:t=>`<div class="c" style="${night('50%','52%')}">${stars(W,H,420,2.2)}${row(eclipse,380,t)}<div class="grain"></div></div>`,
 sacred:t=>`<div class="c" style="${night('50%','52%')}">${stars(W,H,420,2.2)}${row(seedLife,360,t)}<div class="grain"></div></div>`,
};
(async()=>{const b=await chromium.launch();const p=await b.newPage();
 async function shot(html,w,h,out){fs.writeFileSync(D+'/t4.html',`<html><head><style>${css}</style></head><body style="--w:${w}px;--h:${h}px">${html}</body></html>`);await p.setViewportSize({width:w,height:h});await p.goto('file://'+D+'/t4.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:out,type:'jpeg',quality:93});}
 for(const [n,h] of Object.entries(logos)) await shot(h,800,800,`${D}/out4/logo_${n}.jpg`);
 for(const [n,f] of Object.entries(bans)){await shot(f(tE),W,H,`${D}/out4/banner_EN_${n}.jpg`);await shot(f(tK),W,H,`${D}/out4/banner_KR_${n}.jpg`);}
 await b.close();})();
