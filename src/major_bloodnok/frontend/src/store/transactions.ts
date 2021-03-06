import { writable, derived } from "svelte/store";

function createTransactionsStore(cls: string) {
    const { subscribe, set, update } = writable([]);
    let loading = false;
    let offset = 0;

    async function load() {
        if (!loading) {
            loading = true;
            try {
                const url = '/api/' + cls + '?page[offset]=' + offset + '&page[limit]=30';
                const response = await fetch(url);
                if (response.ok) {
                    const data = (await response.json()).data;
                    for (const entry of data) {
                        const parts = entry.attributes.date.split('-');
                        const date = new Date();
                        date.setFullYear(parseInt(parts[0]));
                        date.setMonth(parseInt(parts[1]));
                        date.setDate(parseInt(parts[2]));
                        entry.attributes.date = date;
                    }
                    update((existing) => {
                        return existing.concat(data);
                    });
                    if (data.length > 0) {
                        offset = offset + data.length;
                    }
                }
                loading = false;
            } catch(e) {
                loading = false;
                throw e;
            }
        }
    }

    async function reset() {
        set([]);
        offset = 0;
        await load();
    }

    load();

    return {
        subscribe,
        load,
        reset,
    }
}

export const transactions = createTransactionsStore('transactions');
export const unclassified = createTransactionsStore('uncategorised');
