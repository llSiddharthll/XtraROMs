// Service Worker script
const CACHE_NAME = 'xtraroms-cache-v1';
const urlsToCache = [
  '/',
  '/account/signup/',
  '/account/login/',
  '/custom_roms/',
  '/magisk_modules/',
  '/privacy_policy',
  '/search_roms/',
  '/xtraknowledge/',
  // Add URLs of your template files here
  '/static/images/xlogo.png',
  '/static/images/xbg.png',
  '/static/images/xtrabg.png',
  '/static/images/xtrabg.jpg',
  '/static/images/ss1.png',
  '/static/images/ss2.png',
  '/static/images/ss3.png',
  '/static/images/ss4.png',

  // Add URLs of your static files here
  '/static/output.css'
];

self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - return response
        if (response) {
          return response;
        }

        // Clone the request because requests are stream and can only be consumed once
        const fetchRequest = event.request.clone();

        return fetch(fetchRequest).then(
          function(response) {
            // Check if we received a valid response
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clone the response because responses are stream and can only be consumed once
            const responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(function(cache) {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      })
  );
});
