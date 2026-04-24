{% load static %}
const CACHE_NAME = 'gic-v14';

const PRECACHE_URLS = [
  '{% url "core:offline" %}',
  '{% static "js/tailwind.js" %}',
  '{% static "css/fonts.css" %}',
  '{% static "fonts/material-symbols-rounded.woff2" %}',
  '{% static "fonts/noto-sans-latin.woff2" %}',
  '{% static "fonts/noto-serif-normal-latin.woff2" %}',
  '{% static "fonts/noto-serif-italic-latin.woff2" %}',
  '{% static "images/logo.png" %}',
  '{% static "images/icon-192.png" %}',
  '{% static "images/icon-512.png" %}',
];

// Install: cache each URL individually so one failure doesn't block the rest
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache =>
      Promise.allSettled(
        PRECACHE_URLS.map(url =>
          fetch(url).then(response => {
            if (response.ok) return cache.put(url, response);
          }).catch(() => {})
        )
      )
    )
  );
  self.skipWaiting();
});

// Activate: delete caches from previous versions
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Only handle GET requests
  if (request.method !== 'GET') return;

  // Never intercept admin
  if (url.pathname.startsWith('/admin/')) return;

  // Static assets — cache-first, fall back to network and cache only successful responses
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(request).then(cached => {
        if (cached) return cached;
        return fetch(request).then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
          }
          return response;
        });
      })
    );
    return;
  }

  // Navigation requests — network-first, fall back to offline page
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() =>
        caches.match('{% url "core:offline" %}').then(cached => {
          if (cached) return cached;
          return new Response('<h1>You are offline</h1>', {
            headers: { 'Content-Type': 'text/html' }
          });
        })
      )
    );
    return;
  }
});
