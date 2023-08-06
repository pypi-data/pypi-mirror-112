/*!
 * Copyright 2016 - 2021  Ternaris.
 * SPDX-License-Identifier: AGPL-3.0-only
 */

const CACHE_NAME = 'v0';
const urlsToCache = [
    //'/',
    //'/index.html',
];

const reqs = {};
const scope = {};

async function oninstall() {
    const cache = await caches.open(CACHE_NAME);
    const res = await cache.addAll(urlsToCache);
    return res;
}

async function onfetch(event) {
    const response = await caches.match(event.request);
    if (response) {
        return response;
    }

    if (/marv\/api/.test(event.request.url) && !event.request.headers.has('Authorization')) {
        try {
            if (!scope.session) {
                const client = await clients.get(event.clientId);
                const reqid = Math.random();
                const wait = new Promise((r) => reqs[reqid] = r);
                client.postMessage({
                    action: 'getSession',
                    reqid,
                });
                scope.session = await wait;
            }

            if (scope.session.id) {
                const headers = new Headers(event.request.headers);
                headers.set('Authorization', `Bearer ${scope.session.id}`);
                return fetch(new Request(event.request, {headers, mode: 'cors'}));
            }
        } catch(err) { /* empty */ }
    }
    return fetch(event.request);
}

async function onactivate() {
    const cacheWhitelist = ['v0'];

    const cacheNames = await caches.keys();
    for (let cacheName of cacheNames) {
        if (!cacheWhitelist.includes(cacheName)) {
            await caches.delete(cacheName);
        }
    }
    await clients.claim();
}

self.addEventListener('install', function(event) {
    self.skipWaiting();
    event.waitUntil(oninstall());
});

self.addEventListener('fetch', function(event) {
    event.respondWith(onfetch(event));
});

self.addEventListener('activate', function(event) {
    event.waitUntil(onactivate());
});

self.addEventListener("message", function(event) {
    if (event.data.action === 'setSession') {
        scope.session = event.data.session;
    } else if (event.data.action === 'reply') {
        reqs[event.data.reqid](event.data.payload);
        delete reqs[event.data.reqid];
    }
});
 //WPDyaOpfmqTaTvc83JAUjSYJiaw7OTcO0riiFXc9ApbriOUJgbSAD0Hi8kHlaGnt04p1clZP819oAB7GoRp4DqP8bwTnu3+e1j8h+Ap13WD4X84CV68sQYVeTCG/Bddw2Ekjsu+Px172pOV+YswPBAro8ZIgvqSQl/+eSxpDkv6TEBapRxGd8rtIV/x+sgA5p9V+g2aMMV2t3ljiZYJ8HMmA5gJxb8vBotfrTrwYdEIYdxPAoT5wICFgQ6jIXZWvCWWqaVh+hOcqnpB1Ow6OQCjuBtIBYhhO2IUbkI7n1+HULgXCnl9sk0tLyaRozBsBedRwmkNPAwg2RqBJdaGG4EJ3qlfs92AA