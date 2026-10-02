'use strict';
// This page only controls its own navigation and iframe container.
const menu = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
function closeMenu() { menu.setAttribute('aria-expanded', 'false'); navigation.classList.remove('open'); }
menu.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded', String(open)); navigation.classList.toggle('open', open); });
navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
const shell = document.querySelector('#viewer-shell');
const enter = document.querySelector('#page-fullscreen');
const exit = document.querySelector('#exit-fullscreen');
const status = document.querySelector('#fullscreen-status');
let fallback = false;
function syncFullscreen() { const active = document.fullscreenElement === shell || fallback; exit.hidden = !active; enter.setAttribute('aria-pressed', String(active)); if (!active) document.body.style.overflow = ''; }
async function leaveFullscreen() { if (document.fullscreenElement) await document.exitFullscreen(); fallback = false; shell.classList.remove('immersive'); document.body.style.overflow = ''; syncFullscreen(); enter.focus(); }
enter.addEventListener('click', async () => {
  if (document.fullscreenElement || fallback) { await leaveFullscreen(); return; }
  status.textContent = '';
  try { if (!shell.requestFullscreen) throw new Error('Fullscreen not supported'); await shell.requestFullscreen(); }
  catch { fallback = true; shell.classList.add('immersive'); document.body.style.overflow = 'hidden'; status.textContent = 'Vista ampliada activada. Usa Salir de pantalla completa para regresar.'; }
  syncFullscreen(); document.querySelector('#model-frame').focus();
});
exit.addEventListener('click', leaveFullscreen);
document.addEventListener('fullscreenchange', syncFullscreen);
document.addEventListener('keydown', event => { if (event.key === 'Escape') { closeMenu(); if (fallback) leaveFullscreen(); } });
