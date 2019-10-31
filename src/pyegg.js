async function getCotizacion() {
    const puppeteer = require('puppeteer');
    const browser = await puppeteer.launch({
        headless: false
    });
    
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    
    await page.goto('https://www.brou.com.uy/cotizaciones');
    console.log('jejejejej');
    return window.document.getElementsByClassName('valor')[5].textContent;    
}

