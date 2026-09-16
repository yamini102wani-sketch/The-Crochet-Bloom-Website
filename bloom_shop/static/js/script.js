document.addEventListener("DOMContentLoaded",()=>{document.querySelectorAll(".product-card,.category-card,.feature-card").forEach((el,i)=>{el.style.animationDelay=(i*40)+"ms"});document.querySelectorAll("form").forEach(f=>{f.addEventListener("submit",()=>{const b=f.querySelector("button[type=submit],button:not([type])");if(b&&b.dataset.loading!=="off"){b.dataset.loading="on";setTimeout(()=>b.disabled=false,2500)}})})});
// Prices page search/filter/sort
function filterPriceCards(){
  const q=(document.getElementById('priceSearch')?.value||'').toLowerCase().trim();
  const cat=(document.getElementById('priceCategory')?.value||'').toLowerCase();
  const sort=document.getElementById('priceSort')?.value||'';
  const grid=document.getElementById('priceProductGrid'); if(!grid) return;
  const cards=[...grid.querySelectorAll('.price-product-card')];
  cards.forEach(c=>{c.style.display=(!q||c.dataset.name.includes(q))&&(!cat||c.dataset.category===cat)?'flex':'none';});
  if(sort){
    const visible=cards.filter(c=>c.style.display!=='none');
    visible.sort((a,b)=>sort==='low'?Number(a.dataset.price)-Number(b.dataset.price):Number(b.dataset.price)-Number(a.dataset.price));
    visible.forEach(c=>grid.appendChild(c));
  }
}
document.addEventListener('DOMContentLoaded',()=>{
  ['priceSearch','priceCategory','priceSort'].forEach(id=>document.getElementById(id)?.addEventListener('change',filterPriceCards));
  document.getElementById('priceSearch')?.addEventListener('input',filterPriceCards);
});
