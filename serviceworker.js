// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/offline/',
    '/static/core/css/estilos.css',
    '/static/core/img/pac-man.png',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('offline/');
            })
    )
});

importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-messaging.js');

var firebaseConfig = {
    apiKey: "AIzaSyDH5qX2jtumlAWA7-Jgwa-ic7axrK2vZiI",
    authDomain: "player1-b169d.firebaseapp.com",
    databaseURL: "https://player1-b169d.firebaseio.com",
    projectId: "player1-b169d",
    storageBucket: "player1-b169d.appspot.com",
    messagingSenderId: "355274120665",
    appId: "1:355274120665:web:60965fedfbb9f2f0834dc8"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  
  let messaging = firebase.messaging();

  //programamos la recepción de las notificaciones en segundo plano

  messaging.setBackgroundMessageHandler(function(payload) {

    let title = payload.notification.title;
    let options = {
        body: payload.notification.body,
        icon: payload.notification.icon
    };

    //mostramos la notificacion
    self.serviceWorkerRegistration.showNotification(title, options);
  });
