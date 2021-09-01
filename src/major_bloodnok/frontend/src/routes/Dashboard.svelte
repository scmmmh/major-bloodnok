<script lang="ts">
    import { onMount } from 'svelte';
    import { link } from 'svelte-navigator';

    import Chart from '../components/Chart.svelte';
    import { dashboard } from '../store';

    onMount(() => {
        dashboard.load();
    });

    function convertToDataset(income: Number[], outgoing: Number[]) {
        return [
            {
                label: 'Income',
                data: income,
                backgroundColor: '#00aa00',
            },
            {
                label: 'Outgoing',
                data: outgoing,
                backgroundColor: '#dd0000',
            }
        ]
    }
</script>

<h1 class="sr-only">Dashboard</h1>
<ol class="flex-1 overflow-auto p-4">
    {#each $dashboard as account}
        <li class="w-full md:w-96 md:inline-block border border-gray-200 px-3 py-2">
            <h2 class="text-xl"><a href="/app/account" use:link>{account.name}</a></h2>
            <Chart labels={account.labels} datasets={convertToDataset(account.income, account.outgoing)}/>
        </li>
    {/each}
</ol>
