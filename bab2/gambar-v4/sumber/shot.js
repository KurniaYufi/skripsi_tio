const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2200,height:900}});
for (const [f,h] of [['ens',840],['shap',900]]){await p.setViewportSize({width:2200,height:h});await p.goto('file://'+process.cwd()+'/'+f+'.html');await p.waitForTimeout(300);await p.screenshot({path:f+'.png'});}
await b.close();})();
