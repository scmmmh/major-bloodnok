<script lang="ts">
    import { derived } from 'svelte/store';

    import { categories, transactions } from '../store';

    export let parentId = null;
    let editCategoryId = null;
    let editCategoryTitle = '';
    let editCategoryParentId = '';

    const items = derived(categories, (categories) => {
        return Object.values(categories).filter((category) => {
            if (category.attributes.title === 'Uncategorised') {
                return false;
            } else if (parentId && category.relationships.parent && category.relationships.parent.data.id === parentId) {
                return true;
            } else if (parentId === null && !category.relationships.parent) {
                return true;
            } else {
                return false;
            }
        });
    });

    function editCategory(category: Category) {
        editCategoryId = category.id;
        editCategoryTitle = category.attributes.title;
        if (category.relationships && category.relationships.parent) {
            editCategoryParentId = category.relationships.parent.data.id;
        }
    }

    async function updateCategory(ev: Event) {
        ev.preventDefault();
        await categories.update(editCategoryId, editCategoryTitle, editCategoryParentId);
        await transactions.reset();
        editCategoryId = null;
    }

    categories.load();
</script>

{#if $items.length > 0}
    <ol class="px-2">
        {#each $items as category}
            <li>
                <div>
                    <span class="inline-block pr-8">{category.attributes.title}</span>
                    <button on:click={() => { editCategory(category) }} aria-label="Edit this category">
                        <svg viewBox="0 0 24 24" class="w-6 h-6 text-blue-700 fill-current">
                            <path d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z" />
                        </svg>
                    </button>
                    <button aria-label="Delete this category">
                        <svg viewBox="0 0 24 24" class="w-6 h-6 text-red-700 fill-current">
                            <path d="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z" />
                        </svg>
                    </button>
                </div>
                <svelte:self parentId={category.id}/>
            </li>
        {/each}
    </ol>
{/if}

{#if editCategoryId}
    <div on:click={(ev) => { editCategoryId = null; }} class="fixed top-0 left-0 w-screen h-screen bg-white bg-opacity-70 transition-colors z-10">
        <div on:click={(ev) => { ev.stopPropagation(); }} class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white border border-blue-900 shadow-xl">
            <h3 class="px-3 py-2 border-b border-blue-900 font-bold">Edit a Category</h3>
            <form on:submit={updateCategory} class="px-3 py-2">
                <label class="block font-sm pb-2">Title
                    <input bind:value={editCategoryTitle} type="text" class="block w-96 px-2 py-1 font-normal border border-gray-700"/>
                </label>
                <label class="block font-sm pb-2 relative">Parent
                    <select bind:value={editCategoryParentId} class="block w-96 px-2 py-1 font-formal border border-gray-700">
                        <option value="">-- Top-level Category --</option>
                        {#each Object.values($categories) as category}
                            <option value={category.id}>{category.attributes.title}</option>
                        {/each}
                    </select>
                </label>
                <div class="text-right">
                    <button on:click={(ev) => { ev.preventDefault(); editCategoryId = null; }} class="px-2 py-1 bg-gray-400 hover:bg-gray-300">Don't update</button>
                    <button class="px-2 py-1 bg-blue-700 hover:bg-blue-600 text-white">Update</button>
                </div>
            </form>
        </div>
    </div>
{/if}
