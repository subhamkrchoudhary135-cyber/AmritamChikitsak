/**
 * Service Worker for Sanjivani AI PWA
 * Provides offline form caching and asset resilience in low-bandwidth Indian environments.
 */

const CACHE_NAME = "sanjivani-ai-v1";
const OFFLINE_URLS = [
  "/",
  "/screen",
  "/results",
  "/manifest.json",
  "/globals.css",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(OFFLINE_URLS).catch((err) => {
        console.warn("Service worker cache pre-fetch warning:", err);
      });
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME) {
            return caches.delete(name);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  // Only handle GET requests
  if (event.request.method !== "GET") return;

  // Don't intercept API calls directly — allow the API client's resilient mock fallback to handle network drops
  if (event.request.url.includes("/api/")) return;

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Clone and store in cache if successful
        if (response.status === 200) {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return response;
      })
      .catch(async () => {
        // If offline, check cache
        const cachedResponse = await caches.match(event.request);
        if (cachedResponse) {
          return cachedResponse;
        }
        // Fallback to root or offline page
        if (event.request.mode === "navigate") {
          return caches.match("/");
        }
        return new Response("Network offline", { status: 503, statusText: "Offline" });
      })
  );
});
