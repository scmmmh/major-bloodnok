<script lang="ts">
    import { categories } from '../store';

    export let transaction: Transaction;

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

    function amountFormat(direction: string, amount: number) {
        let result = '';
        if (direction === 'out') {
            result = result + '-';
        }
        result = result + amount.toFixed(2);
        return result;
    }

    async function categoryHierarchyList(id: string): Promise<Category[]> {
        const category = await categories.lookup(id);
        if (category.relationships.parent) {
            return (await categoryHierarchyList(category.relationships.parent.data.id)).concat([category]);
        } else {
            return [category];
        }
    }
</script>

<div class="w-28 text-center">
    <div class="text-lg">{transaction.attributes.date.getDate()}</div>
    <div class="text-sm">{monthStr(transaction.attributes.date.getMonth())}</div>
</div>
<div class="flex-1">
    <p class="text-lg">{transaction.attributes.description}</p>
    {#await categoryHierarchyList(transaction.relationships.category.data.id) then categoryList}
        <ol>
            {#each categoryList as category}
                <li class="inline-block px-2 rounded bg-blue-700 text-white mr-2">{category.attributes.title}</li>
            {/each}
        </ol>
    {/await}
</div>
<div class="w-32 text-xl font-bold text-right pr-4 self-center {transaction.attributes.direction === 'in' ? 'text-green-600' : ''}">
    &pound; {amountFormat(transaction.attributes.direction, transaction.attributes.amount)}
</div>
