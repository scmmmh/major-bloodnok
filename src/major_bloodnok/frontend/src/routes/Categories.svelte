<script lang="ts">
    import { categories, transactions } from "../store";
    import CategoryTreeItem from "../components/CategoryTreeItem.svelte";

    let addCategory = false;
    let newCategoryTitle = '';
    let newCategoryParentId = '';

    function showAddCategory() {
        addCategory = true;
        newCategoryTitle = '';
        newCategoryParentId = '';
    }

    async function createCategory(ev: Event) {
        ev.preventDefault();
        await categories.create(newCategoryTitle, newCategoryParentId);
        await transactions.reset();
        addCategory = false;
    }
</script>

<h1 class="sr-only">Categories</h1>
<div class="overflow-auto p-4">
    <div class="mb-4">
        <button on:click={showAddCategory} class="px-3 py-2 bg-blue-700 text-white hover:bg-blue-600">Add a category</button>
    </div>
    <CategoryTreeItem/>
</div>

{#if addCategory}
    <div on:click={(ev) => { addCategory = false; }} class="fixed top-0 left-0 w-screen h-screen bg-white bg-opacity-70 transition-colors z-10">
        <div on:click={(ev) => { ev.stopPropagation(); }} class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white border border-blue-900 shadow-xl">
            <h3 class="px-3 py-2 border-b border-blue-900 font-bold">Add a Category</h3>
            <form on:submit={createCategory} class="px-3 py-2">
                <label class="block font-sm pb-2">Title
                    <input bind:value={newCategoryTitle} type="text" class="block w-96 px-2 py-1 font-normal border border-gray-700"/>
                </label>
                <label class="block font-sm pb-2 relative">Parent
                    <select bind:value={newCategoryParentId} class="block w-96 px-2 py-1 font-formal border border-gray-700">
                        <option value="">-- Top-level Category --</option>
                        {#each Object.values($categories) as category}
                            <option value={category.id}>{category.attributes.title}</option>
                        {/each}
                    </select>
                </label>
                <div class="text-right">
                    <button on:click={(ev) => { ev.preventDefault(); addCategory = false; }} class="px-2 py-1 bg-gray-400 hover:bg-gray-300">Don't add</button>
                    <button class="px-2 py-1 bg-blue-700 hover:bg-blue-600 text-white">Add</button>
                </div>
            </form>
        </div>
    </div>
{/if}
