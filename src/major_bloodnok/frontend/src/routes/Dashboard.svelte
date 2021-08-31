<script lang="ts">
    import { onMount } from 'svelte';

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

<h1>Dashboard</h1>
<ol>
    {#each $dashboard as account}
        <li class="w-80">
            <h2>{account.name}</h2>
            <Chart labels={account.labels} datasets={convertToDataset(account.income, account.outgoing)}/>
        </li>
    {/each}
</ol>
