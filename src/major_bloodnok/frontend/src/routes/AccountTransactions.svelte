<script lang="ts">
    import { transactions } from '../store';

    function monthStr(month: number) {
        if (month === 1) {
            return 'January';
        } else if (month === 2) {
            return 'February';
        } else if (month === 3) {
            return 'March';
        } else if (month === 4) {
            return 'April';
        } else if (month === 5) {
            return 'May';
        } else if (month === 6) {
            return 'June';
        } else if (month === 7) {
            return 'July';
        } else if (month === 8) {
            return 'August';
        } else if (month === 9) {
            return 'September';
        } else if (month === 10) {
            return 'October';
        } else if (month === 11) {
            return 'November';
        } else if (month === 12) {
            return 'December';
        }
    }

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
            <div class="w-28 text-center">
                <div class="text-lg">{transaction.attributes.date.getDate()}</div>
                <div class="text-sm">{monthStr(transaction.attributes.date.getMonth())}</div>
            </div>
            <div class="flex-1">
                <p class="text-lg">{transaction.attributes.description}</p>
            </div>
            <div class="w-32 text-xl font-bold text-right pr-4 self-center {transaction.attributes.direction === 'in' ? 'text-green-600' : ''}">
                &pound; {transaction.attributes.direction === 'out' ? '-' : ''}{transaction.attributes.amount}
            </div>
        </li>
    {/each}
</ol>
