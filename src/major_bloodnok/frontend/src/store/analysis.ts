import { writable } from "svelte/store";

function createJSONAPIStore(cls: string) {
    const entries = writable({} as {[x:string]: JSONAPIItem});
    let loading = false;

    async function load() {
        if (!loading) {
            loading = true;
            try {
                let url = '/api/' + cls;
                const response = await fetch(url);
                if (response.ok) {
                    const data = (await response.json()).data as JSONAPIItem[];
                    entries.set(Object.fromEntries(data.map((category) => {
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

    return {
        subscribe: entries.subscribe,
        load,
    }
}

export const analysisTimePeriods = createJSONAPIStore('analysis-time-periods');
