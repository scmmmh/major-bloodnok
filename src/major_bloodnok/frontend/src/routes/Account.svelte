<script lang="ts">
    import { useLocation, useResolve, Route, navigate } from 'svelte-navigator';
    import Dropzone from "svelte-file-dropzone";

    import NavItem from '../components/NavItem.svelte';

    const location = useLocation();
    const resolve = useResolve();

    async function handleFilesSelect(e) {
        const { acceptedFiles } = e.detail;
        for (const file of (acceptedFiles as File[])) {
            const data = await file.text();
            const response = await fetch('/api/transactions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'text/csv'
                },
                body: data
            });
        }
        navigate(resolve('/account'));
    }
</script>

<h1 class="sr-only">Account</h1>
<div class="flex flex-row flex-1 overflow-auto p-4">
    <nav class="flex-0 w-48 bg-blue-200">
        <ul>
            <li><NavItem href="/account" class="px-3 py-2 {$location.pathname === '/account' ? 'bg-blue-800 text-white' : ''}">Transactions</NavItem></li>
            <li><NavItem href="/account/upload" class="px-3 py-2 {$location.pathname === '/account/upload' ? 'bg-blue-800 text-white' : ''}">Upload</NavItem></li>
        </ul>
    </nav>
    <div class="flex-1 px-4">
        <Route path="/">
            <h2 class="sr-only">Transactions</h2>
            <table>
                <thead>
                    <th>Category</th>
                    <th>Date</th>
                </thead>
            </table>
        </Route>
        <Route path="/upload">
            <h2 class="sr-only">Upload</h2>
            <Dropzone on:drop={handleFilesSelect} accept=".csv,text/csv"/>
        </Route>
    </div>
</div>
