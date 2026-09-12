console.log("[Ridgane] Vanilla JS loaded");
document.addEventListener('click', e => { 
  if(e.target.dataset.update) 
    document.querySelector('[year]').textContent = new Date().getUTCFullYear(); 
});
