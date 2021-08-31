import { writable } from "svelte/store";

function createCollectionStore() {
    const { subscribe, set } = writable([]);
    let loading = false;

    async function load() {
        if (!loading) {
            loading = true;
            try {
                const response = await fetch('/api/dashboards');
                if (response.ok) {
                    set((await response.json()).data);
                }
                loading = false;
            } catch(e) {
                loading = false;
                throw e;
            }
        }
    }

    load();

    return {
        subscribe,
        load,
    }
}

export const dashboard = createCollectionStore();
