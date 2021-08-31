<script lang="ts">
    import { link, Route } from 'svelte-navigator';
</script>

<h1 class="flex-0 text-2xl px-4 py-3">Account</h1>
<div class="flex flex-row flex-1 overflow-auto px-4">
    <nav class="flex-0 w-40">
        <ul class="pr-2">
            <li><a href="/app/account" use:link>Transactions</a></li>
            <li><a href="/app/account/upload" use:link>Upload</a></li>
        </ul>
    </nav>
    <div class="flex-1">
        <Route path="/">
            <h2 class="text-xl sr-only">Transactions</h2>
            <table>
                <thead>
                    <th>Category</th>
                    <th>Date</th>
                </thead>
            </table>
        </Route>
        <Route path="/upload">
            <h2 class="text-xl sr-only">Upload</h2>
            <form>
                <label>Upload transactions
                    <input type="file" class="block"/>
                </label>
            </form>
        </Route>
    </div>
</div>
