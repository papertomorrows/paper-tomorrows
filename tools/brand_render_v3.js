const { chromium } = require('playwright'); const fs=require('fs'); const D=__dirname;
const css=`
@font-face{font-family:Corm;src:url(CormorantGaramond.ttf)}@font-face{font-family:CormI;src:url(CormorantGaramond-Italic.ttf)}
@font-face{font-family:Inter;src:url(Inter.ttf)}@font-face{font-family:Cinzel;src:url(Cinzel.ttf)}
@font-face{font-family:Pre;src:url(Pretendard-Light.otf);font-weight:300}@font-face{font-family:Pre;src:url(Pretendard-Medium.otf);font-weight:500}@font-face{font-family:Pre;src:url(Pretendard-SemiBold.otf);font-weight:600}
*{margin:0;padding:0;box-sizing:border-box}body{width:var(--w);height:var(--h);overflow:hidden;background:#000}
.c{position:relative;width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden}
.grain{position:absolute;inset:0;opacity:.12;mix-blend-mode:overlay;pointer-events:none;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.mesh{position:absolute;inset:-20%;filter:blur(60px)}
`;
// aurora mesh background
const aurora=`<div class="mesh" style="background:radial-gradient(40% 50% at 25% 35%,#5b3df5 0%,transparent 70%),radial-gradient(35% 45% at 75% 30%,#ff7a59 0%,transparent 70%),radial-gradient(45% 55% at 60% 80%,#1fb6a6 0%,transparent 70%),radial-gradient(50% 60% at 20% 85%,#c13dd6 0%,transparent 70%),#0a0a1a"></div>`;
const aurora2=`<div class="mesh" style="background:radial-gradient(45% 55% at 30% 40%,#6c4cff 0%,transparent 70%),radial-gradient(40% 50% at 72% 60%,#ff8a5c 0%,transparent 70%),radial-gradient(40% 50% at 50% 100%,#ffd36e 0%,transparent 70%),#0b0b18"></div>`;
// pixel art helpers
function pixels(map,size,colors){const rows=map.trim().split('\n');const n=rows[0].length;let s=`<div style="display:grid;grid-template-columns:repeat(${n},${size}px);gap:0">`;for(const r of rows)for(const ch of r)s+=`<div style="width:${size}px;height:${size}px;background:${colors[ch]||'transparent'};${colors[ch]&&ch!=='.'?'box-shadow:0 0 '+size*0.8+'px '+(colors[ch])+'55':''}"></div>`;return s+'</div>';}
const player=`
y...yy...y
y..yyyy..y
.y.yyyy.y.
.y..yy..y.
..yyyyyy..
...yyyy...
...yyyy...
...yyyy...
...y..y...
..yy..yy..`;
const sparkle=`
....w....
....w....
...www...
.wwwwwww.
wwwwwwwww
.wwwwwww.
...www...
....w....
....w....`;
const lotusPlay=`<svg viewBox="0 0 100 100" width="360" height="360"><path d="M28 16 L84 50 L28 84 Z" fill="none" stroke="#fff" stroke-width="3.2" stroke-linejoin="round"/><path d="M44 58 C44 46 50 40 50 40 C50 40 56 46 56 58 C53 61 47 61 44 58Z M50 61 C40 62 34 56 33 50 C40 49 46 52 50 61Z M50 61 C60 62 66 56 67 50 C60 49 54 52 50 61Z" fill="#fff" transform="translate(-8,0)"/></svg>`;
const logos={
 A_aurora_play:`<div class="c">${aurora}<svg viewBox="0 0 100 100" width="330" height="330" style="position:relative;margin-left:40px"><path d="M26 14 Q26 8 32 11 L84 44 Q90 50 84 56 L32 89 Q26 92 26 86 Z" fill="#fff"/></svg><div class="grain"></div></div>`,
 B_pixel_player:`<div class="c" style="background:radial-gradient(circle at 50% 45%,#1c1640,#07060f 70%)">${pixels(player,46,{y:'#ffd36e'})}<div class="grain"></div></div>`,
 C_pixel_spark:`<div class="c">${aurora2}<div style="position:relative">${pixels(sparkle,48,{w:'#ffffff'})}</div><div class="grain"></div></div>`,
 E_wordmark:`<div class="c" style="background:#0b0b14"><div style="font-family:Inter;font-weight:800;font-size:150px;line-height:.86;letter-spacing:-6px;color:#fff;text-align:left">PLAY<br>YOUR<br><span style="background:linear-gradient(90deg,#8f6bff,#ff8a5c);-webkit-background-clip:text;color:transparent">OWN</span><br>GAME</div><div class="grain"></div></div>`,
 F_cinzel:`<div class="c" style="background:radial-gradient(circle at 50% 40%,#16203d,#05070f 75%)"><div style="width:600px;height:600px;border:2px solid #c9a55c;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-direction:column"><div style="font-family:Cinzel;font-weight:600;font-size:200px;color:#e8cf8f;letter-spacing:10px">PY</div><div style="font-family:Cinzel;font-size:30px;letter-spacing:12px;color:#c9a55c;margin-top:-6px">OWN GAME</div></div><div class="grain"></div></div>`,
};
const bans={
 aurora:(t,s)=>`<div class="c">${aurora}<div style="position:relative;text-align:center">${t}${s}</div><div class="grain"></div></div>`,
 pixel:(t,s)=>`<div class="c" style="background:radial-gradient(ellipse 70% 80% at 50% 50%,#1c1640,#07060f 75%)"><div style="display:flex;align-items:center;gap:90px">${pixels(player,20,{y:'#ffd36e'})}<div style="text-align:center">${t}${s}</div>${pixels(sparkle,16,{w:'#fff'})}</div><div class="grain"></div></div>`,
};
const tE=`<div style="font-family:Inter;font-weight:800;font-size:118px;letter-spacing:-4px;color:#fff">PLAY YOUR <span style="background:linear-gradient(90deg,#b49bff,#ffb08a);-webkit-background-clip:text;color:transparent">OWN</span> GAME</div>`;
const sE=`<div style="font-family:Inter;font-weight:500;font-size:34px;letter-spacing:12px;color:rgba(255,255,255,.75);margin-top:26px">MIND · SOUL · UNIVERSE</div>`;
const tK=`<div style="font-family:Pre;font-weight:600;font-size:140px;letter-spacing:-2px;color:#fff">당신만의 <span style="background:linear-gradient(90deg,#b49bff,#ffb08a);-webkit-background-clip:text;color:transparent">게임</span></div>`;
const sK=`<div style="font-family:Pre;font-weight:500;font-size:40px;letter-spacing:14px;color:rgba(255,255,255,.75);margin-top:26px">마음 · 영혼 · 우주</div>`;
(async()=>{const b=await chromium.launch();const p=await b.newPage();
 async function shot(html,w,h,out){fs.writeFileSync(D+'/t3.html',`<html><head><style>${css}</style></head><body style="--w:${w}px;--h:${h}px">${html}</body></html>`);await p.setViewportSize({width:w,height:h});await p.goto('file://'+D+'/t3.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:out,type:'jpeg',quality:93});}
 for(const [n,h] of Object.entries(logos)) await shot(h,800,800,`${D}/out3/logo_${n}.jpg`);
 for(const [n,f] of Object.entries(bans)){await shot(f(tE,sE),2560,1440,`${D}/out3/banner_EN_${n}.jpg`);await shot(f(tK,sK),2560,1440,`${D}/out3/banner_KR_${n}.jpg`);}
 await b.close();})();
