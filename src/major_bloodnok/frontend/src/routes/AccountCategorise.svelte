<script lang="ts">
    import TransactionComponent from '../components/Transaction.svelte';
    import { unclassified, categories, transactions } from '../store';

    let selectedTransaction = null as Transaction;
    let newRulePattern = '';
    let newRuleDirection = '';
    let newRuleCategory = null;
    let newRuleCategoryTitle = '';
    let categoryLookup = [];

    function scroll(ev: Event) {
        const elem = (ev.target as HTMLElement);
        if (elem.scrollHeight - elem.scrollTop < elem.clientHeight * 2) {
            unclassified.load();
        }
    }

    function selectTransaction(transaction: Transaction) {
        selectedTransaction = transaction;
        newRulePattern = selectedTransaction.attributes.description.replace('*', '\\*');
        newRuleDirection = selectedTransaction.attributes.direction;
        newRuleCategory = null;
        newRuleCategoryTitle = '';
        categoryLookup = [];
    }

    async function addRule(ev: Event) {
        ev.preventDefault();
        if (newRulePattern !== '' && newRuleDirection !== '' && newRuleCategory !== null) {
            if (newRuleCategory.id === '') {
                const response = await fetch('/api/categories', {
                    method: 'POST',
                    body: JSON.stringify(newRuleCategory)
                });
                newRuleCategory = (await response.json()).data;
            }
            await fetch('/api/rules', {
                method: 'POST',
                body: JSON.stringify({
                    type: 'rules',
                    attributes: {
                        pattern: newRulePattern,
                        direction: newRuleDirection,
                    },
                    relationships: {
                        category: {
                            data: {
                                type: 'categories',
                                id: newRuleCategory.id,
                            }
                        }
                    }
                })
            });
            selectedTransaction = null;
            await unclassified.reset();
            await categories.load();
            await transactions.reset();
        }
    }

    function lookupCategory(ev: KeyboardEvent) {
        const value = (ev.target as HTMLInputElement).value;
        if (value.trim().length > 0) {
            let exactMatch = false;
            const temp = Object.values($categories).filter((category) => {
                exactMatch = exactMatch || category.attributes.title.toLowerCase() == value.toLowerCase();
                return category.attributes.title.toLowerCase().indexOf(value.toLowerCase()) >= 0;
            });
            if (!exactMatch) {
                temp.push({
                    type: 'categories',
                    id: '',
                    attributes: {
                        title: value,
                    },
                    relationships: {
                    }
                });
            }
            categoryLookup = temp;
        } else {
            categoryLookup = [];
        }
    }

    function selectNewRuleCategory(category: Category) {
        newRuleCategory = category;
        categoryLookup = [];
        newRuleCategoryTitle = category.attributes.title;
    }

    categories.load();
</script>

<h2 class="sr-only">Transactions</h2>
<ol on:scroll={scroll} class="w-full h-full overflow-auto">
    {#each $unclassified as transaction}
        <li class="flex py-2 odd:bg-blue-100">
            <TransactionComponent transaction={transaction}/>
            <div class="flex-0 self-center px-2">
                <button on:click={() => { selectTransaction(transaction); }} class="p-2 text-black hover:text-blue-900 transition-colors">
                    <svg viewBox="0 0 24 24" class="w-8 h-8 fill-current">
                        <path d="M17,13H13V17H11V13H7V11H11V7H13V11H17M19,3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3Z" />
                    </svg>
                </button>
            </div>
        </li>
    {/each}
</ol>

{#if selectedTransaction}
    <div on:click={(ev) => { selectedTransaction = null; }} class="fixed top-0 left-0 w-screen h-screen bg-white bg-opacity-70 transition-colors z-10">
        <div on:click={(ev) => { ev.stopPropagation(); }} class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white border border-blue-900 shadow-xl">
            <h3 class="px-3 py-2 border-b border-blue-900 font-bold">Add a Rule</h3>
            <form on:submit={addRule} class="px-3 py-2">
                <label class="block font-sm pb-2">Description Pattern
                    <input bind:value={newRulePattern} type="text" class="block w-96 px-2 py-1 font-normal border border-gray-700"/>
                </label>
                <label class="block font-sm pb-2">Direction
                    <select bind:value={newRuleDirection} class="block w-96 px-2 py-1 font-normal border border-gray-700">
                        <option value='in'>Income</option>
                        <option value='out'>Outgoing</option>
                    </select>
                </label>
                <label class="block font-sm pb-2 relative">Category
                    <input on:keyup={lookupCategory} bind:value={newRuleCategoryTitle} type="text" class="block w-96 px-2 py-1 font-normal border border-gray-700"/>
                    {#if categoryLookup.length > 0}
                        <ol class="absolute w-full top-full left-0 border border-gray-700 bg-white z-10">
                            {#each categoryLookup as category}
                                <li><button on:click={() => { selectNewRuleCategory(category) }} class="block px-3 py-2 w-full text-left hover:bg-blue-700 hover:text-white transition-colors">{category.attributes.title}</button></li>
                            {/each}
                        </ol>
                    {/if}
                </label>
                <div class="text-right">
                    <button on:click={(ev) => { ev.preventDefault(); selectedTransaction = null; }} class="px-2 py-1 bg-gray-400 hover:bg-gray-300">Don't add</button>
                    <button class="px-2 py-1 bg-blue-700 hover:bg-blue-600 text-white">Add</button>
                </div>
            </form>
        </div>
    </div>
{/if}
