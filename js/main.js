'use strict';
const $ = (selector, parent = document) => parent.querySelector(selector);
const $$ = (selector, parent = document) => [...parent.querySelectorAll(selector)];
const el = (tag, className, text) => { const node = document.createElement(tag); if (className) node.className = className; if (text) node.textContent = text; return node; };
// Relative paths keep this site portable under a GitHub project subdirectory.
function safeUrl(value) { if (!value || typeof value !== 'string') return ''; try { const url = new URL(value, document.baseURI); return ['http:', 'https:'].includes(url.protocol) ? url.href : ''; } catch { return ''; } }
function setLink(link, path, {download = false, newTab = false, enabled = true} = {}) {
  const url = safeUrl(path);
  if (!url || !enabled) { link.removeAttribute('href'); link.setAttribute('aria-disabled', 'true'); link.setAttribute('role', 'link'); link.title = 'Pendiente de incorporar'; return; }
  link.href = url; link.removeAttribute('aria-disabled'); link.removeAttribute('role'); link.removeAttribute('title');
  if (download) link.setAttribute('download', '');
  if (newTab) { link.target = '_blank'; link.rel = 'noopener'; link.title = 'Abrir en una pestaña nueva'; }
}
function imageNode(item, eager = false) {
  const img = el('img'); img.src = safeUrl(item.src); img.alt = item.alt || item.title || item.label;
  img.width = item.width; img.height = item.height; img.loading = eager ? 'eager' : 'lazy'; img.decoding = 'async';
  if (eager) img.setAttribute('fetchpriority', 'high');
  // Optional responsive variants; no remote assets required.
  if (item.srcset) { img.srcset = item.srcset; img.sizes = item.sizes || '100vw'; }
  img.addEventListener('error', () => { const fallback = el('div', 'media-error', item.label || item.title); fallback.setAttribute('role', 'img'); fallback.setAttribute('aria-label', `${item.alt || item.label}. Archivo no disponible`); img.replaceWith(fallback); }, {once:true});
  return img;
}
function imageLabel(item) { const label = el('span', 'media-label', item.label); label.setAttribute('aria-hidden', 'true'); return label; }
const menuButton = $('.menu-toggle');
function closeMenu() { menuButton.setAttribute('aria-expanded', 'false'); $('#navigation').classList.remove('open'); }
menuButton.addEventListener('click', () => { const open = menuButton.getAttribute('aria-expanded') !== 'true'; menuButton.setAttribute('aria-expanded', String(open)); $('#navigation').classList.toggle('open', open); });
$$('#navigation a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
let gallery = [], current = 0, returnFocus = null;
const lightbox = $('#lightbox'), videoDialog = $('#video-dialog');
function lockScroll() { document.body.style.overflow = 'hidden'; }
function unlockScroll() { document.body.style.overflow = ''; if (returnFocus?.isConnected) returnFocus.focus(); }
function showImage(index) {
  current = (index + gallery.length) % gallery.length; const item = gallery[current];
  const img = $('#lightbox-image'); img.src = safeUrl(item.src); img.alt = item.alt || item.title; img.width = item.width; img.height = item.height;
  $('#lightbox-title').textContent = item.title || item.label;
  $('#lightbox-count').textContent = `${String(current + 1).padStart(2, '0')} / ${String(gallery.length).padStart(2, '0')}`;
  const link = $('#lightbox-download'); link.hidden = !safeUrl(item.download); setLink(link, item.download, {download:true});
  $('#previous').hidden = $('#next').hidden = gallery.length < 2;
}
function openImage(index, trigger) { returnFocus = trigger; showImage(index); lightbox.showModal(); lockScroll(); $('.close-dialog', lightbox).focus(); }
$('#previous').addEventListener('click', () => showImage(current - 1));
$('#next').addEventListener('click', () => showImage(current + 1));
lightbox.addEventListener('keydown', event => { if (event.key === 'ArrowLeft') { event.preventDefault(); showImage(current - 1); } if (event.key === 'ArrowRight') { event.preventDefault(); showImage(current + 1); } if (event.key === 'Home') { event.preventDefault(); showImage(0); } if (event.key === 'End') { event.preventDefault(); showImage(gallery.length - 1); } });
for (const dialog of [lightbox, videoDialog]) {
  dialog.addEventListener('keydown', event => {
    if (event.key !== 'Tab') return;
    const focusable = $$('button:not([disabled]), a[href], video[controls], [tabindex="0"]', dialog).filter(node => node.getClientRects().length);
    const first = focusable[0], last = focusable[focusable.length - 1];
    if (!first) { event.preventDefault(); return; }
    if (event.shiftKey && (document.activeElement === first || !dialog.contains(document.activeElement))) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && (document.activeElement === last || !dialog.contains(document.activeElement))) { event.preventDefault(); first.focus(); }
  });
  $('.close-dialog', dialog).addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => { if (dialog === videoDialog) { const player = $('video', dialog); if (player) { player.pause(); player.removeAttribute('src'); player.load(); } $('#video-player').replaceChildren(); } unlockScroll(); });
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
}
function openVideo(item, trigger) {
  returnFocus = trigger; $('#video-dialog-title').textContent = item.title; const container = $('#video-player'); container.replaceChildren();
  if (safeUrl(item.src)) { const video = el('video'); video.controls = true; video.preload = 'metadata'; video.playsInline = true; video.src = safeUrl(item.src); if (safeUrl(item.poster)) video.poster = safeUrl(item.poster); if (item.captions) { const track = el('track'); track.kind = 'captions'; track.src = safeUrl(item.captions); track.srclang = item.language || 'es'; track.label = 'Subtítulos'; video.append(track); } video.append(el('p', '', 'Tu navegador no puede reproducir este vídeo.')); container.append(video); }
  else { const pending = el('div', 'pending-video'); if (safeUrl(item.poster)) pending.append(imageNode({src:item.poster,alt:`Miniatura de ${item.title}`,width:1920,height:1080})); pending.append(el('strong', '', item.label || item.title), el('p', '', 'Vídeo pendiente de incorporar')); container.append(pending); }
  videoDialog.showModal(); lockScroll(); $('.close-dialog', videoDialog).focus();
}
function render(data) {
  const images = [...data.images].sort((a,b) => a.order - b.order);
  for (const section of ['hero','intro','viewer','location']) { const item = images.find(image => image.section === section); if (item) $(`[data-media="${section}"]`).append(imageNode(item, section === 'hero'), imageLabel(item)); }
  gallery = images.filter(image => image.section === 'gallery');
  gallery.forEach((item,index) => { const figure = el('figure', 'gallery-item'); const button = el('button', 'gallery-button'); button.type = 'button'; button.setAttribute('aria-label', `Ampliar ${item.title || item.label}`); button.style.aspectRatio = `${item.width} / ${item.height}`; button.append(imageNode(item), imageLabel(item)); button.addEventListener('click', () => openImage(index, button)); const caption = el('figcaption', 'image-caption'); caption.append(el('span','',item.title || item.label), el('span','','↗')); figure.append(button,caption); $('#gallery').append(figure); });
  [...data.videos].sort((a,b) => a.order - b.order).forEach(item => {
    const card = el('article', 'video-card'), preview = el('button', 'video-preview'); preview.type = 'button'; preview.style.aspectRatio = `${item.width || 1920} / ${item.height || 1080}`; preview.setAttribute('aria-label', `Reproducir ${item.title}`);
    if (safeUrl(item.poster)) preview.append(imageNode({src:item.poster,alt:`Miniatura de ${item.title}`,width:item.width || 1920,height:item.height || 1080,label:item.title})); else preview.append(el('span','video-placeholder',item.title));
    preview.append(imageLabel({label:item.label || item.title})); const play = el('span', 'play-symbol', '▶'); play.setAttribute('aria-hidden','true'); preview.append(play); preview.addEventListener('click',()=>openVideo(item,preview));
    const meta = el('div','video-meta'); meta.append(el('h3','',item.title)); if (item.duration) meta.append(el('span','video-duration',item.duration));
    const actions = el('div','video-actions'), playButton = el('button','','REPRODUCIR ↗'), download = el('a','text-link','DESCARGAR ↓'); playButton.type = 'button'; playButton.addEventListener('click',()=>openVideo(item,playButton)); setLink(download,item.download,{download:true}); actions.append(playButton,download); card.append(preview,meta,actions); $('#video-grid').append(card);
  });
  const presentation = data.downloads.find(file => file.id === data.presentationId);
  $$('[data-presentation]').forEach(link => {
    const viewing = link.dataset.presentation === 'view';
    const resource = viewing ? data.presentationView : presentation;
    setLink(link, resource?.path, {enabled: resource?.available === true, download: !viewing, newTab: viewing});
  });
  $$('[data-viewer]').forEach(link => setLink(link, data.viewerUrl)); $('#viewer-status').hidden = !!safeUrl(data.viewerUrl);
  data.downloads.forEach(file => {
    if (file.id === data.presentationId) {
      const row = el('div', 'download-row presentation-row');
      const actions = el('div', 'doc-actions');
      const view = el('a', 'text-link presentation-primary', 'VER PRESENTACIÓN');
      const pdf = el('a', 'text-link', 'VER / DESCARGAR PDF');
      setLink(view, data.presentationView?.path, {enabled: data.presentationView?.available === true, newTab: true});
      setLink(pdf, file.path, {enabled: file.available === true, newTab: true});
      actions.append(view, pdf);
      row.append(el('span', 'file-type', file.type), el('span', 'file-name', file.title), el('span', 'file-size', file.size), actions);
      $('#download-list').append(row);
      return;
    }
    const row = el('div','download-row'), link = el('a','text-link','DESCARGAR ↓'); setLink(link,file.path,{download:true,enabled:file.available === true}); if (file.available !== true) link.setAttribute('aria-label',`Descargar ${file.title}: pendiente de incorporar`); else link.setAttribute('aria-label',`Descargar ${file.title}`); row.append(el('span','file-type',file.type),el('span','file-name',file.title),el('span','file-size',file.size),link); $('#download-list').append(row); });
}
fetch('data/media.json', {cache:'no-cache'}).then(response => { if (!response.ok) throw new Error('No se pudo cargar media.json'); return response.json(); }).then(data => { if (![data.images,data.videos,data.downloads].every(Array.isArray)) throw new Error('Formato de media.json incorrecto'); render(data); }).catch(error => { $('#load-status').textContent = 'No se pudieron cargar los medios. Comprueba data/media.json y abre la web mediante HTTP.'; console.error(error); });
