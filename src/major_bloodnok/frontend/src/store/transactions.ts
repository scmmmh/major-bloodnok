import { writable, derived } from "svelte/store";

function createTransactionsStore() {
    const { subscribe, set } = writable([]);
    let loading = false;

    async function load() {
        if (!loading) {
            loading = true;
            try {
                const response = await fetch('/api/transactions');
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
                    set(data);
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

export const transactions = createTransactionsStore();
export const unclassified = derived(transactions, (transactions) => {
    return transactions;
});
