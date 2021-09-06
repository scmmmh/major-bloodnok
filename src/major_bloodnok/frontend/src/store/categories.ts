import { writable, get } from "svelte/store";

const uniqueFetchPromises = {};

async function uniqueFetch(url: string) {
    if (uniqueFetchPromises[url] === undefined) {
        const promise = new Promise((resolve, reject) => {
            fetch(url).then((response) => {
                delete uniqueFetchPromises[url];
                response.json().then((data) => {
                    resolve(data.data);
                });
            }, (err) => {
                delete uniqueFetchPromises[url];
                reject(err);
            });
        });
        uniqueFetchPromises[url] = promise;
        return promise;
    } else {
        return uniqueFetchPromises[url];
    }
}

function createJSONAPIStore(cls) {
    const categories = writable({});
    let loading = false;

    async function load() {
        if (!loading) {
            loading = true;
            try {
                let url = '/api/' + cls;
                const response = await fetch(url);
                if (response.ok) {
                    const data = (await response.json()).data as JSONAPIItem[];
                    categories.set(Object.fromEntries(data.map((category) => {
                        return [category.id, category];
                    })));
                }
                loading = false;
            } catch(e) {
                loading = false;
                throw e;
            }
        }
    }

    async function loadSingle(id: string) {
        const item = get(categories)[id];
        if (item) {
            return item;
        } else {
            const item = await uniqueFetch('/api/' + cls + '/' + id);
            categories.update((categories) => {
                categories[id] = item;
                return categories;
            })
            return item;
        }
    }

    async function lookup(id: string) {
        let category = get(categories)[id];
        if (category) {
            return category;
        } else {
            category = await loadSingle(id);
            if (category) {
                return category;
            }
            throw Error('Lookup failed');
        }
    }

    return {
        subscribe: categories.subscribe,
        load,
        loadSingle,
        lookup,
    }
}

export const categories = createJSONAPIStore('categories');
