<script lang="ts">
    import { onDestroy } from 'svelte';
    import { derived } from 'svelte/store';

    import { analysisTimePeriods, categories } from '../store';

    const sortedAnalysisTimePeriods = derived(analysisTimePeriods, (analysisTimePeriods) => {
        const values = Object.values(analysisTimePeriods);
        values.sort((a, b) => {
            if ((a.attributes.value as string).indexOf('-') >= 0 && (b.attributes.value as string).indexOf('-') >= 0) {
                if (a.attributes.value > b.attributes.value) {
                    return -1;
                } else if (a.attributes.value < b.attributes.value) {
                    return 1;
                }
            } else if ((a.attributes.value as string).indexOf('-') >= 0 && (b.attributes.value as string).indexOf('-') < 0) {
                return -1;
            } else if ((a.attributes.value as string).indexOf('-') < 0 && (b.attributes.value as string).indexOf('-') >= 0) {
                return 1;
            } else {
                if (a.attributes.value > b.attributes.value) {
                    return 1;
                } else if (a.attributes.value < b.attributes.value) {
                    return -1;
                }
            }
            return 0;
        })
        return values;
    });

    let analysisItems = [];
    let timePeriod = '';
    let direction = 'out';
    let category = '';
    let totalAmount = 0;

    async function loadAnalysis() {
        if (timePeriod !== '') {
            const analysis = await fetch('/api/analysis?filter[timePeriod]=' + timePeriod + '&filter[direction]=' + direction + '&filter[category]=' + category);
            analysisItems = (await analysis.json()).data;
            totalAmount = 0;
            for (const analysisItem of analysisItems) {
                totalAmount = totalAmount + analysisItem.attributes.amount;
            }
        }
    }

    analysisTimePeriods.load();
    categories.load();

    loadAnalysis();
    const unsubscribeCategories = categories.subscribe((categories) => { loadAnalysis(); });
    const unsubcribeAnalysisTimePeriods = sortedAnalysisTimePeriods.subscribe((analysisTimePeriods) => {
        if (analysisTimePeriods.length > 0) {
            timePeriod = analysisTimePeriods[0].id;
        }
        loadAnalysis();
    });

    onDestroy(() => {
        unsubscribeCategories();
        unsubcribeAnalysisTimePeriods();
    });
</script>

<h2 class="sr-only">Analysis</h2>
<div class="flex flex-col overflow-hidden h-full">
    <form class="flex-0 flex flex-row">
        <label class="pr-4"><span class="sr-only">Time Period</span>
            <select bind:value={timePeriod} on:change={loadAnalysis} class="border px-3 py-2">
                {#each $sortedAnalysisTimePeriods as timePeriod}
                    <option value={timePeriod.attributes.value}>{timePeriod.attributes.label}</option>
                {/each}
            </select>
        </label>
        <label class="pr-4"><span class="sr-only">Direction</span>
            <select bind:value={direction} on:change={loadAnalysis} class="border px-3 py-2">
                <option value="in">Income</option>
                <option value="out">Outgoing</option>
            </select>
        </label>
        <label><span class="sr-only">Filter by</span>
            <select bind:value={category} on:change={loadAnalysis} class="border px-3 py-2">
                <option value="">--- Top-level Categories ---</option>
                {#each Object.values($categories) as category}
                    <option value={category.id}>{category.attributes.title}</option>
                {/each}
            </select>
        </label>
    </form>
    <div class="flex-1 overflow-auto">
        <table class="mt-4">
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>
                {#each analysisItems as analysisItem}
                    <tr class="odd:bg-gray-300">
                        <td class="px-3 py-2">{analysisItem.attributes.title}</td>
                        <td class="text-right px-3 py-2">&pound; {analysisItem.attributes.amount.toFixed(2)}</td>
                    </tr>
                {/each}
            </tbody>
            <tfoot>
                <tr>
                    <td class="italic px-3 py-2">Total</td>
                    <td class="text-right px-3 py-2">&pound; {totalAmount.toFixed(2)}</td>
                </tr>
            </tfoot>
        </table>
    </div>
</div>
