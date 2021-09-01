<script lang="ts">
    import { useLocation, Route } from 'svelte-navigator';

    import NavItem from '../components/NavItem.svelte';
    import AccountTransactions from './AccountTransactions.svelte';
    import AccountUpload from './AccountUpload.svelte';
    import { unclassified } from '../store';

    const location = useLocation();
</script>

<h1 class="sr-only">Account</h1>
<div class="flex flex-row flex-1 overflow-auto p-4">
    <nav class="flex-0 w-48 bg-blue-200">
        <ul>
            <li><NavItem href="/account" class="px-3 py-2 {$location.pathname === '/account' ? 'bg-blue-800 text-white' : ''}">Transactions</NavItem></li>
            {#if $unclassified.length > 0}
                <li><NavItem href="/account/classify" class="px-3 py-2 {$location.pathname === '/account/classify' ? 'bg-blue-800 text-white' : ''}">Classify <span class="px-1 rounded-full bg-blue-500">{$unclassified.length}</span></NavItem></li>
            {/if}
            <li><NavItem href="/account/upload" class="px-3 py-2 {$location.pathname === '/account/upload' ? 'bg-blue-800 text-white' : ''}">Upload</NavItem></li>
        </ul>
    </nav>
    <div class="flex-1 px-4">
        <Route path="/"><AccountTransactions/></Route>
        <Route path="/upload"><AccountUpload/></Route>
    </div>
</div>
