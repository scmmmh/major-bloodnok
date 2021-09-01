<script lang="ts">
    import { useResolve, navigate } from 'svelte-navigator';
    import Dropzone from "svelte-file-dropzone";

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

<h2 class="sr-only">Upload</h2>
<Dropzone on:drop={handleFilesSelect} accept=".csv,text/csv"/>
