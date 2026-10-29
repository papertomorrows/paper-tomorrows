const { chromium } = require('playwright');
const fs=require('fs'); const D=__dirname;
const css=`
@font-face{font-family:Corm;src:url(CormorantGaramond.ttf)}
@font-face{font-family:CormI;src:url(CormorantGaramond-Italic.ttf)}
@font-face{font-family:Inter;src:url(Inter.ttf)}
@font-face{font-family:Gowun;src:url(GowunBatang-Regular.ttf)}
@font-face{font-family:Pre;src:url(Pretendard-Light.otf);font-weight:300}
@font-face{font-family:Pre;src:url(Pretendard-Regular.otf);font-weight:400}
*{margin:0;padding:0;box-sizing:border-box}
body{width:var(--w);height:var(--h);overflow:hidden}
.c{position:relative;width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden}
.grain{position:absolute;inset:0;opacity:.13;mix-blend-mode:overlay;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
`;
const ink=`background:radial-gradient(ellipse 60% 55% at 50% 52%,#1d2340 0%,#0d1020 60%,#07080f 100%)`;
const dusk=`background:linear-gradient(180deg,#1b1f3b 0%,#3a3566 38%,#a4778a 72%,#e9b99a 100%)`;
const sand=`background:radial-gradient(ellipse at 50% 40%,#f6efe4 0%,#ece1cf 70%,#e2d4bd 100%)`;
const orbit=(s,col,dot)=>`<svg width="${s}" height="${s}" viewBox="0 0 100 100" style="position:absolute"><circle cx="50" cy="50" r="46" fill="none" stroke="${col}" stroke-width=".35"/><circle cx="${50+46*Math.cos(-0.9)}" cy="${50+46*Math.sin(-0.9)}" r="1.6" fill="${dot}"/></svg>`;
const logos={
 logo_1_monogram:`<div class="c" style="${ink}"><div style="font-family:CormI;font-weight:300;font-size:560px;color:#efe6d6;line-height:1;margin-top:-40px">P</div><div style="position:absolute;width:26px;height:26px;border-radius:50%;background:#d9b46a;left:540px;top:470px"></div><div class="grain"></div></div>`,
 logo_2_orbit:`<div class="c" style="${ink}">${orbit(560,'#d9b46a','#f3d58c')}<div style="width:120px;height:120px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#fff6df,#d9b46a 60%,#8a6a2c)"></div><div class="grain"></div></div>`,
 logo_3_dusk_play:`<div class="c" style="${dusk}"><svg width="300" height="300" viewBox="0 0 100 100"><path d="M30 18 Q30 12 36 15 L82 45 Q87 50 82 55 L36 85 Q30 88 30 82 Z" fill="none" stroke="#fff8ee" stroke-width="2.2" stroke-linejoin="round"/></svg><div class="grain"></div></div>`,
 logo_4_sand_monogram:`<div class="c" style="${sand}"><div style="font-family:Corm;font-weight:400;font-size:300px;color:#1c1f2e;letter-spacing:-6px">p<span style="font-family:CormI;color:#9a7433">y</span></div><div class="grain" style="opacity:.08"></div></div>`,
};
const sub=(t,col)=>`<div style="font-family:Inter;font-weight:400;font-size:30px;letter-spacing:14px;color:${col};margin-top:34px">${t}</div>`;
const subK=(t,col)=>`<div style="font-family:Pre;font-weight:300;font-size:36px;letter-spacing:16px;color:${col};margin-top:34px">${t}</div>`;
const titleE=(col,acc)=>`<div style="font-family:Corm;font-weight:300;font-size:150px;color:${col};letter-spacing:2px">Play Your <span style="font-family:CormI;color:${acc}">Own</span> Game</div>`;
const titleK=(col,acc)=>`<div style="font-family:Gowun;font-size:130px;color:${col};letter-spacing:8px">당신만의 <span style="color:${acc}">게임</span></div>`;
const banners={
 ink:(t,s)=>`<div class="c" style="${ink}">${orbit(900,'rgba(217,180,106,.45)','#f3d58c')}<div style="position:relative;text-align:center">${t('#f1e9da','#d9b46a')}${s('rgba(241,233,218,.6)')}</div><div class="grain"></div></div>`,
 dusk:(t,s)=>`<div class="c" style="${dusk}"><div style="position:relative;text-align:center">${t('#fff8ee','#fff8ee')}${s('rgba(255,248,238,.75)')}</div><div class="grain"></div></div>`,
 sand:(t,s)=>`<div class="c" style="${sand}"><div style="position:relative;text-align:center">${t('#1c1f2e','#9a7433')}${s('rgba(28,31,46,.55)')}</div><div class="grain" style="opacity:.08"></div></div>`,
};
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage();
 async function shot(html,w,h,out){fs.writeFileSync(D+'/t.html',`<html><head><style>${css}</style></head><body style="--w:${w}px;--h:${h}px">${html}</body></html>`);await p.setViewportSize({width:w,height:h});await p.goto('file://'+D+'/t.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:out,type:'jpeg',quality:93});}
 for(const [n,h] of Object.entries(logos)) await shot(h,800,800,`${D}/out/${n}.jpg`);
 for(const [n,f] of Object.entries(banners)){
  await shot(f(titleE,c=>sub('MIND · SOUL · UNIVERSE',c)),2560,1440,`${D}/out/banner_EN_${n}.jpg`);
  await shot(f(titleK,c=>subK('마음 · 영혼 · 우주',c)),2560,1440,`${D}/out/banner_KR_${n}.jpg`);
 }
 await b.close();
})();
