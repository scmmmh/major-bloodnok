<script lang="ts">
    import Transaction from '../components/Transaction.svelte';
    import { transactions } from '../store';

    function scroll(ev: Event) {
        const elem = (ev.target as HTMLElement);
        if (elem.scrollHeight - elem.scrollTop < elem.clientHeight * 2) {
            transactions.load();
        }
    }
</script>

<h2 class="sr-only">Transactions</h2>
<ol on:scroll={scroll} class="w-full h-full overflow-auto">
    {#each $transactions as transaction}
        <li class="flex py-2 odd:bg-blue-100">
            <Transaction transaction={transaction}/>
        </li>
    {/each}
</ol>
